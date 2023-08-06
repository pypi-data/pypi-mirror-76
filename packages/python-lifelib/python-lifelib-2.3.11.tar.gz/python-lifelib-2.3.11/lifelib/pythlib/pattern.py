import os
from .lowlevel import *
from numbers import Integral
from .crt import chinese_remainder, large_primes
from .samples import download_synthesis as dsynth
from .registry import register_pattern_callback

def randfill(item, shape):
    '''
    Create a numpy array of a specified shape with specified probabilities
    of being each item.
    '''

    import numpy as np
    if isinstance(item, float):
        item = {0: 1.0 - item, 1: item}

    p = np.array(list(item.values()), dtype=float)
    p = p / np.sum(p)
    v = np.array(list(item.keys()), dtype=np.uint64)

    return np.random.choice(v, p=p, size=shape)


class Pattern(object):

    def __init__(self, session, ptr, owner):

        self.ptr = ptr
        self.lifelib = session.lifelib
        self.session = session
        self.owner = owner
        self.comments = []

        session.pattern_ptrs.add(ptr)

    def __del__(self):

        if self.ptr in self.session.pattern_ptrs:
            self.lifelib('DeletePattern', self.ptr)
            self.session.pattern_ptrs.remove(self.ptr)

    def __repr__(self):

        logdiam = self.lifelib('GetDiameterOfPattern', self.ptr)
        beszel_index = self.lifelib('GetBeszelIndex', self.ptr)
        ulqoma_index = self.lifelib('GetUlqomaIndex', self.ptr)
        rule = self.getrule()

        return ("<Pattern(logdiam=%d, beszel_index=%d, ulqoma_index=%d, rule=%s) owned by %r>" % (logdiam,
            beszel_index, ulqoma_index, rule, self.owner))

    def digest(self):

        return self.lifelib('GetPatternDigest', self.ptr)

    def octodigest(self):

        return self.lifelib('GetPatternOctodigest', self.ptr)

        '''
        od = [self.digest()]
        for o in ["rot270", "rot180", "rot90", "flip_x", "flip_y", "swap_xy", "swap_xy_flip"]:
            od.append(self(o).digest())
        od = sorted(set(od))
        return sum([(2*i+1)*j for (i, j) in enumerate(od)]) & (2**64 - 1)
        '''

    def advance(self, numgens, exponent=0):

        self.lifelib.ensure_limit(exponent, numgens, 'Number of generations')

        temp = self

        while (numgens != 0):

            t = tzcount(numgens)
            if (t > 0):
                numgens = numgens >> t
                exponent = exponent + t

            max_num = 2 ** 30

            x = int(numgens if (abs(numgens) < max_num) else (numgens % max_num))

            newptr = self.lifelib('AdvancePattern', temp.ptr, x, exponent)
            temp = Pattern(self.session, newptr, self.owner)
            numgens = numgens - x

        return temp

    def _solid(self, state, exponent=0):

        if (state < 0) or (state >= (2**64)):
            raise ValueError("States must be integers in the interval [0, 2^64 - 1].")

        temp = self.owner.pattern("", self.getrule())

        while (state != 0):

            t = tzcount(state)
            if (t > 0):
                state = state >> t
                exponent = exponent + t

            max_num = 2 ** 30

            x = int(state % max_num)

            newptr = self.lifelib('GetSolidForPattern', self.ptr, x, exponent)
            temp += Pattern(self.session, newptr, self.owner)
            state = state - x

        return temp

    def _semisolid(self, flags):

        newptr = self.lifelib('GetSemisolidForPattern', self.ptr, flags)
        return Pattern(self.session, newptr, self.owner)

    def _boolean_mutable(self, other, op):

        self.lifelib('BooleanPatternMutable', self.ptr, other.ptr, op)
        return self

    def _bitshift(self, shift):

        newptr = self.lifelib('BitshiftPattern', self.ptr, shift)
        return Pattern(self.session, newptr, self.owner)

    def _boolean_immutable(self, other, op):

        newptr = self.lifelib('BooleanPatternImmutable', self.ptr, other.ptr, op)
        return Pattern(self.session, newptr, self.owner)

    def __iand__(self, other):
        return self._boolean_mutable(other, 0)

    def __ior__(self, other):
        return self._boolean_mutable(other, 1)

    def __ixor__(self, other):
        return self._boolean_mutable(other, 2)

    def __isub__(self, other):
        return self._boolean_mutable(other, 3)

    def __iadd__(self, other):
        return self._boolean_mutable(other, 1)

    def __imul__(self, other):
        return self._boolean_mutable(other, 4)

    def __imatmul__(self, other):
        return self._boolean_mutable(other, 7)

    def __and__(self, other):
        return self._boolean_immutable(other, 0)

    def __or__(self, other):
        return self._boolean_immutable(other, 1)

    def __xor__(self, other):
        return self._boolean_immutable(other, 2)

    def __sub__(self, other):
        return self._boolean_immutable(other, 3)

    def __add__(self, other):
        return self._boolean_immutable(other, 1)

    def __mul__(self, other):
        return self._boolean_immutable(other, 4)

    def __matmul__(self, other):
        return self._boolean_immutable(other, 7)

    def __lshift__(self, other):
        return self._bitshift(other)

    def __rshift__(self, other):
        return self._bitshift(-other)

    def convolve(self, other, exclusive=False):
        return self._boolean_immutable(other, (6 if exclusive else 5))

    def disjunct(self, other, exclusive=False):
        return self._boolean_immutable(other, (2 if exclusive else 1))

    def __pow__(self, other):
        if (other <= 0):
            raise ValueError("Can only raise patterns to positive integer powers")
        elif (other == 1):
            return self
        else:
            return (self * (self ** (other - 1)))

    # These implement the 'subset' partial order defined on sets:

    def __eq__(self, other):
        return bool(self.lifelib('PatternEquality', self.ptr, other.ptr))

    def __ne__(self, other):
        return not (self == other)

    def __le__(self, other):
        return ((self & other) == self)

    def __ge__(self, other):
        return ((self & other) == other)

    def __lt__(self, other):
        return (self != other) and (self <= other)

    def __gt__(self, other):
        return (self != other) and (self >= other)

    def nonempty(self):
        return bool(self.lifelib('PatternNonempty', self.ptr))

    def empty(self):
        return not self.nonempty()

    __nonzero__ = nonempty
    __bool__ = nonempty

    def stream(self, data_or_filename):

        if isinstance(data_or_filename, list):
            data_or_filename = str(data_or_filename)

        newptr = self.lifelib('MakeSpaceshipStream', self.ptr, data_or_filename)
        return Pattern(self.session, newptr, self.owner)

    def transform(self, tfm):

        transforms = ["flip", "rot180", "identity", "transpose", "flip_x", "flip_y",
                        "rot90", "rot270", "swap_xy", "swap_xy_flip", "rcw", "rccw"]

        if tfm not in transforms:
            raise ValueError("Transformation must be one of %s" % str(transforms))

        newptr = self.lifelib('TransformPattern', self.ptr, tfm)
        return Pattern(self.session, newptr, self.owner)

    def __copy__(self):

        newptr = self.lifelib('CopyPattern', self.ptr)
        return Pattern(self.session, newptr, self.owner)

    def shift(self, x, y, exponent=0):

        if not isinstance(x, Integral):
            raise TypeError("shift arguments must be integers")

        if not isinstance(y, Integral):
            raise TypeError("shift arguments must be integers")

        self.lifelib.ensure_limit(exponent, x, 'Horizontal shift')
        self.lifelib.ensure_limit(exponent, y, 'Vertical shift')

        temp = self

        while ((x | y) != 0):

            t = tzcount(x | y)
            if (t > 0):
                x = x >> t
                y = y >> t
                exponent = exponent + t

            max_num = 2 ** 30
            dx = int(x if (abs(x) < max_num) else (x % max_num))
            dy = int(y if (abs(y) < max_num) else (y % max_num))
            newptr = self.lifelib('ShiftPattern', temp.ptr, dx, dy, exponent)
            temp = Pattern(self.session, newptr, self.owner)
            x -= dx
            y -= dy

        return temp

    def centre(self):

        if self.empty():
            return self

        bbox = self.getrect()
        return self.shift(-(bbox[0] + (bbox[2] // 2)), -(bbox[1] + (bbox[3] // 2)))

    def _getbound(self, direction, pixelsize=None, offset=None):

        if pixelsize is None:
            logdiam = self.lifelib('GetDiameterOfPattern', self.ptr)
            pixelsize = (logdiam // 30) * 30
            offset = -(1 << (logdiam - 1))

        b = int(self.lifelib('GetPatternBound', self.ptr, direction, pixelsize)) % (2 ** 30)

        if (pixelsize == 0):
            return b + offset

        b = b << pixelsize

        x = self(-b, 0) if (direction % 2 == 0) else self(0, -b)
        x = x[offset:offset + (1 << pixelsize),:] if (direction % 2 == 0) else x[:,offset:offset + (1 << pixelsize)]

        return b + x._getbound(direction, pixelsize - 30, offset)

    def component_containing(self, seed=None, halo='ooo$ooo$ooo!'):

        if seed is None:
            seed = self.onecell()

        if not isinstance(halo, Pattern):
            halo = self.owner.pattern(halo, self.getrule()).centre()

        if isinstance(seed, tuple):
            seed = self.owner.pattern('o!', self.getrule())(seed[0], seed[1])

        newptr = self.lifelib('FindConnectedComponent', seed.ptr, self.ptr, halo.ptr)
        return Pattern(self.session, newptr, self.owner)

    def onecell(self):

        newptr = self.lifelib('GetOneCell', self.ptr)
        return Pattern(self.session, newptr, self.owner)

    def layers(self):

        return self.owner.deunify(self)

    def components(self, halo='ooo$ooo$ooo!'):

        ccs = []
        x = self

        while (x.nonempty()):

            cc = x.component_containing(halo=halo)
            x = x - cc
            ccs.append(cc)

        return ccs

    def match(self, live, dead=None, halo=None):

        if halo is not None:
            if not isinstance(halo, Pattern):
                halo = self.owner.pattern(halo, self.getrule()).centre()
            dead = live.convolve(halo)

        if dead is None:
            newptr = self.lifelib('MatchLive', self.ptr, live.ptr)
        else:
            corona = dead - live
            newptr = self.lifelib('MatchLiveAndDead', self.ptr, live.ptr, corona.ptr)
        return Pattern(self.session, newptr, self.owner)

    def replace(self, live, replacement, dead=None, n_phases=0, stepsize=1, orientations=['identity'], **kwargs):

        if n_phases > 0:
            temp = self
            for _ in range(n_phases):
                temp = temp[stepsize].replace(live, replacement, dead=dead, orientations=orientations, **kwargs)
            return temp

        if orientations == 'rotate4reflect':
            orientations = ["rot270", "rot180", "rot90", "identity",
                            "flip_x", "flip_y", "swap_xy", "swap_xy_flip"]

        replaced = self.owner.pattern("", self.getrule())
        matched  = self.owner.pattern("", self.getrule())

        for o in orientations:

            ro = replacement.transform(o)
            lo = live.transform(o)
            do = dead.transform(o) if (dead is not None) else dead

            m = self.match(lo, dead=do, **kwargs)
            matched  += m.convolve(lo)
            replaced += m.convolve(ro)

        return (self - matched) + replaced

    def __call__(self, *args):

        if (len(args) > 3):
            raise TypeError("Usage: pattern(8, -5) or pattern('rccw') or pattern('rot90', 7, 3)")

        temp = self.__copy__()

        if ((len(args) % 2) == 1):
            temp = temp.transform(args[0])

        if (len(args) >= 2):
            temp = temp.shift(args[-2], args[-1])

        return temp

    def pdetect_or_advance(self, maxexp=24):

        newptr = self.lifelib('FindPeriodOrAdvance', self.ptr, maxexp)

        if newptr[0]:
            return Pattern(self.session, newptr, self.owner)
        else:
            dt = self.lifelib('GetDTOfPattern', self.ptr)
            dx = self.lifelib('GetDXOfPattern', self.ptr)
            dy = self.lifelib('GetDYOfPattern', self.ptr)
            return {'period': dt, 'displacement': (dx, dy)}

    def getrule(self):

        return self.lifelib('GetRuleOfPattern', self.ptr, [2048])

    def phase_wechsler(self, fn='GetWechslerOfPattern'):

        x = self.lifelib(fn, self.ptr, [2048], 2048)
        if x.startswith('!'):
            buflen = int(x[1:])
            x = self.lifelib(fn, self.ptr, [buflen], buflen)
        return x

    def oscar(self, maxexp=24, eventual_oscillator=True, verbose=True, return_apgcode=False):

        logdiam = self.lifelib('GetDiameterOfPattern', self.ptr)

        if (logdiam > 60):
            raise ValueError("Pattern is too large for oscillation detection.")

        x = self
        for exponent in range(8, maxexp+2, 2):
            if (verbose) and (exponent > 8):
                print("Checking periodicity with exponent %d..." % exponent)
            y = x.pdetect_or_advance(exponent)
            if isinstance(y, dict):
                if (return_apgcode):
                    y['apgcode'] = x.phase_wechsler('GetApgcodeOfPattern')
                return y
            if (eventual_oscillator):
                x = y

        if (verbose):
            print("Oscillation not detected (try increasing maxexp?)")
        return {}

    def write_rle(self, filename, header=None, footer=None, comments=None, file_format='rle', save_comments=True):

        filename = os.path.abspath(filename)

        if header is None:
            header = ''

        if footer is None:
            footer = ''

        if save_comments:
            if comments is None:
                comments = self.comments
            if hasattr(comments, 'splitlines'):
                comments = comments.splitlines()
            comments = [(x if x.startswith('#C ') else ('#C ' + x)) for x in comments]
            header += ''.join([('%s\n' % x) for x in comments])

        llc = 'SavePatternRLE' if (file_format[-3:].lower() == 'rle') else 'SavePatternMC'
        self.lifelib(llc, self.ptr, filename, header, footer)

    def write_file(self, filename, file_format='deduce', compressed=False, tempfile='tempfile', **kwargs):

        if file_format == 'deduce':
            compressed = (filename[-3:] == '.gz')
            filebase = filename[:-3] if compressed else filename
            file_format = filebase[-3:]
        elif file_format[-3:] == '.gz':
            compressed = True
            file_format = file_format[:-3]

        if compressed:
            self.write_rle(tempfile, file_format=file_format, **kwargs)
            import gzip
            import shutil
            with open(tempfile, 'rb') as f_in:
                with gzip.open(filename, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            try:
                os.remove(tempfile)
            except OSError:
                pass
        else:
            self.write_rle(filename, file_format=file_format, **kwargs)

    # This seems to have better symmetry with Lifetree.load() so we
    # include it as an alias for Pattern.write_file():
    save = write_file


    def rle_string(self, filename=None, autoremove=True):

        if filename is None:
            filename = self.session.newfloat('pattern') + '.rle'

        self.write_rle(filename)

        with open(filename, 'rb') as f:
            rs = regstring(f.read())

        if autoremove:
            try:
                os.remove(filename)
            except OSError:
                pass

        return rs


    def viewer(self, filename=None, width=480, height=480, base64=True,
                lv_config='#C [[ THEME 6 GRID GRIDMAJOR 0 ]]', autoremove=True, edit=True):

        if filename is None:
            filename = self.session.newfloat('viewer') + '.html'

        header = '<html><head><meta name="LifeViewer" content="rle code"></head><body>'
        header += '<div class="rle"><div style="display:none;"><code id="code2">\n'
        footer = '#C [[ WIDTH %d HEIGHT %d ]]\n' % (width, height)
        footer += '</code></div>\n<canvas width="%d" height="%d" style="margin-left:1px;"></canvas></div>\n' % (width+16, height+16)
        footer += "<script type='text/javascript' src='https://gol.hatsya.co.uk/js/lv-plugin.js'></script>\n"

        if edit:
            # Generate a unique identifier for the IFrame, so that the Jupyter
            # notebook knows which LifeViewer has been updated with Ctrl+S.
            from uuid import uuid4
            saveid = str(uuid4())

            # Track when the (invisible!) RLE element is changed, and signal
            # those changes in a message from the IFrame to the notebook. We
            # can catch these messages in the notebook itself.
            footer += '''<script>
var targetNode = document.getElementById('code2');
var config = { attributes: true, childList: true, subtree: true };
var callback = function(mutationsList, observer) {
    console.log("DOM mutated.");
    parent.postMessage({ rle: targetNode.innerHTML, uuid: "%s" }, "*");
};
var observer = new MutationObserver(callback);
observer.observe(targetNode, config);
</script>''' % saveid

            # Register this pattern in the registry:
            register_pattern_callback(saveid, self)

        footer += '</body></html>\n'

        self.write_rle(filename, header, lv_config + '\n' + footer)

        if base64:

            from base64 import b64encode

            with open(filename, 'rb') as f:
                b64html = regstring(b64encode(f.read()))
            source = 'data:text/html;base64,%s' % b64html

            if autoremove:
                try:
                    os.remove(filename)
                except OSError:
                    pass

        else:
            source = filename

        from IPython.display import IFrame

        return IFrame(source, width=width+32, height=height+32)

    def __getitem__(self, x):

        if isinstance(x, Integral):
            return self.advance(x)
        elif isinstance(x, tuple) and isinstance(x[0], Integral) and isinstance(x[1], Integral):
            left = x[0]
            top = x[1]
            relevant_cell = self[left:left+1,top:top+1].shift(-left, -top)
            return self.lifelib('GetOriginState', relevant_cell.ptr)
        elif isinstance(x, tuple):
            left = x[0].start
            right = x[0].stop
            top = x[1].start
            bottom = x[1].stop

            subrect = self
            bigenough = self

            onecell = self.owner.pattern("o!", self.getrule())

            if left is not None:
                bigenough = bigenough + onecell.shift(left, 0)
            if right is not None:
                bigenough = bigenough + onecell.shift(right-1, 0)
            if top is not None:
                bigenough = bigenough + onecell.shift(0, top)
            if bottom is not None:
                bigenough = bigenough + onecell.shift(0, bottom-1)

            if left is not None:
                subrect = subrect & bigenough._semisolid(10).shift(left, 0)
            if right is not None:
                subrect = subrect & bigenough._semisolid(5).shift(right, 0)
            if top is not None:
                subrect = subrect & bigenough._semisolid(12).shift(0, top)
            if bottom is not None:
                subrect = subrect & bigenough._semisolid(3).shift(0, bottom)

            return subrect
        elif hasattr(x, 'ctypes'):

            logdiam = self.lifelib('GetDiameterOfPattern', self.ptr)
            if (logdiam >= 64):
                # Ensure we can safely use int64 arithmetic:
                self64 = self[-(2**63):(2**63), -(2**63):(2**63)]
            else:
                self64 = self

            import numpy as np
            x = np.ascontiguousarray(x, dtype=np.int64)
            n = len(x)
            y = np.zeros((n,), dtype=np.uint64, order='C')
            y = self.lifelib('GetCells', self64.ptr, n, x, y)
            return y
        else:
            raise TypeError("operator[] accepts either a generation (int) or a pair of slices")

    def _subpops(self, n, ps):

        if (ps < 4):
            raise ValueError('log2 of pixel size must be at least 4.')

        logdiam = self.lifelib('GetDiameterOfPattern', self.ptr)
        il = n + ps
        if (logdiam > il):
            self64 = self[-(2**(il-1)):(2**(il-1)), -(2**(il-1)):(2**(il-1))]
        else:
            self64 = self

        import numpy as np
        y = np.zeros((2**n, 2**n), dtype=np.uint64, order='C')
        y = self.lifelib('GetSubpops', self64.ptr, n, ps, y)
        return y

    def coords(self):

        p = self.population
        import numpy as np
        y = np.zeros((p,2), dtype=np.int64, order='C')
        y = self.lifelib('GetCoords', self.ptr, y)
        return y

    def destream(self, other):

        import numpy as np
        oscr = self.oscar()
        disp = np.array(list(oscr['displacement']))
        p = oscr['period']

        offsets = []

        for i in range(p):
            c = other.match(self[i], halo="b3o$5o$5o$5o$b3o!").coords()
            offsets.append(np.dot(c, disp) * p + i * np.dot(disp, disp))

        offsets = np.concatenate(offsets)
        offsets.sort() # in-place
        offsets = np.diff(offsets)[::-1] // np.dot(disp, disp)
        return ([0] + list(offsets) + [0])

    def __setitem__(self, x, item):

        if hasattr(x, 'ctypes'):
            import numpy as np
            x = np.ascontiguousarray(x, dtype=np.int64)
            n = len(x)
            y = np.ascontiguousarray(item, dtype=np.uint64)

            if (len(x) != len(y)):
                raise ValueError('Incompatible shapes for setcells.')

            self.lifelib('SetCells', self.ptr, n, x, y)
            return

        x = tuple([(slice(y, y + 1) if isinstance(y, Integral) else y) for y in x])

        self -= self[x]

        if isinstance(item, float) or isinstance(item, dict):
            shape = (x[0].stop - x[0].start, x[1].stop - x[1].start)
            item = randfill(item, shape)

        if hasattr(item, 'ctypes'):
            import numpy as np
            xr = np.arange(x[0].start, x[0].stop)
            yr = np.arange(x[1].start, x[1].stop)
            coords = np.ascontiguousarray(np.array(list(map(np.ravel, np.meshgrid(xr, yr)))).T, dtype=np.int64)
            values = np.ascontiguousarray(np.ravel(item), dtype=np.uint64)
            if (len(coords) != len(values)):
                raise ValueError('Incompatible shapes for setcells.')

            self.lifelib('SetCells', self.ptr, len(coords), coords, values)
            return
        elif isinstance(item, Integral):
            if (item == 0):
                return
            onecell = self.owner.pattern("o!", self.getrule())
            bigenough = onecell(x[0].start, x[1].start) + onecell(x[0].stop - 1, x[1].stop - 1)
            item = bigenough._solid(item)

        self += item[x]

    def getrect(self):

        if self.empty():
            # An empty pattern does not possess a well-defined bounding box:
            return None

        logdiam = self.lifelib('GetDiameterOfPattern', self.ptr)

        if (logdiam > 60):
            # Slower bigint solution:
            bounds = [self._getbound(i) for i in range(4)]
            bbox = [bounds[0], bounds[1], bounds[2] + 1 - bounds[0], bounds[3] + 1 - bounds[1]]
        else:
            # Fast int64 solution:
            bbox = self.lifelib('GetPatternBox', self.ptr, [1, 4])

        return bbox

    @property
    def bounding_box(self):

        return self.getrect()

    @property
    def population(self):

        logdiam = self.lifelib('GetDiameterOfPattern', self.ptr)
        nprimes = (logdiam + 14) // 15
        relprimes = large_primes[:nprimes]
        populations = [self.lifelib('GetPopulationOfPattern', self.ptr, p) for p in relprimes]
        return chinese_remainder(relprimes, populations)

    @property
    def wechsler(self):

        return self.phase_wechsler()

    @property
    def apgcode(self):

        return self.oscar(return_apgcode=True, eventual_oscillator=False, verbose=False)['apgcode']

    def download_samples(self, **kwargs):

        return self.owner.download_samples(self.apgcode, self.getrule(), **kwargs)

    def download_synthesis(self, tempfile='tempfile.rle', **kwargs):

        rle = dsynth(self.apgcode, self.getrule(), tempfile=tempfile, **kwargs)

        if rle is None:
            synth = None
        else:
            synth = self.owner.load(tempfile)

        try:
            os.remove(tempfile)
        except OSError:
            pass

        return synth

    @property
    def period(self):

        return self.oscar(eventual_oscillator=False, verbose=False)['period']

    @property
    def displacement(self):

        return self.oscar(eventual_oscillator=False, verbose=False)['displacement']
