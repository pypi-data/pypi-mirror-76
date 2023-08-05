/**
* Represents a forest of balanced N-ary trees.
*
* Trees are compressed, so identical branches are represented by indices
* to the same location in memory. Empty branches occupy no memory at all.
*
* The leaves are of (hashable) type LK, but we can also hang information
* of type LV from a leaf and NV from a non-leaf. Since identical branches
* occupy the same memory, you cannot hang distinct information from
* identical branches.
*
* I should be an unsigned integer type (usually uint32_t, but this would
* need to be uint64_t if the forest occupies more than 4 billion nodes*).
* Note that using uint64_t instead of uint32_t would result in the forest
* occupying twice as much memory, so this is discouraged unless you do
* actually need more than 4 billion nodes -- unlikely unless you have at
* least 200 gigabytes of RAM.
*
* *Nodes in each layer have separate sets of indices, so you can have up
* to 4 billion nodes in each layer.
*/

#pragma once

#include "nicearray.h"
#include "kivtable.h"
#include <stdint.h>
#include <iostream>
#include <cstdarg>
#include <string>
#include <limits>
#include <map>
#include <memory>
#include <vector>

namespace apg {

    template<typename I>
    struct hypernode {
        I index;
        I index2;
        uint32_t depth;

        explicit hypernode(I index, I index2, uint32_t depth) {
            this->index = index;
            this->index2 = index2;
            this->depth = depth;
        }

        explicit hypernode(I index, uint32_t depth) {
            this->index = index;
            this->index2 = 0;
            this->depth = depth;
        }

        explicit hypernode() {
            this->index = -1;
            this->index2 = 0;
            this->depth = 0;
        }

        bool empty() const { return ((index == 0) && (index2 == 0)); }
        bool nonempty() const { return ((index != 0) || (index2 != 0)); }
        bool operator==(const hypernode<I> &other) const {
            return ((depth == other.depth) && (index == other.index) && (index2 == other.index2));
        }
    };

    template<typename I, int N, typename NV, typename LK, typename LV>
    class hypertree {

        // We store a kivtable for each layer in our hypertree:
        std::vector<std::unique_ptr<kivtable<nicearray<I, N>, I, NV>>> nonleaves;
        kivtable<LK, I, LV> leaves;

        public:

        uint64_t total_bytes() const {
            uint64_t n = leaves.total_bytes();
            for (unsigned int i = 0; i < nonleaves.size(); i++) {
                n += nonleaves[i]->total_bytes();
            }
            return n;
        }

        // Maps symbol to a node in the hypertree:
        uint64_t hcounter = 0;
        std::map<uint64_t, hypernode<I> > ihandles;
        std::map<std::string, hypernode<I> > handles;

        // Wrapper for nonleaves.ind2ptr:
        kiventry<nicearray<I, N>, I, NV>* ind2ptr_nonleaf(uint32_t depth, I index) {
            return nonleaves[depth-1]->ind2ptr(index);
        }

        // Wrapper for leaves.ind2ptr:
        kiventry<LK, I, LV>* ind2ptr_leaf(I index) {
            return leaves.ind2ptr(index);
        }

        // Get the nth child of a particular node:
        hypernode<I> getchild(hypernode<I> parent, uint32_t n) {
            if (parent.depth == 0 || parent.index == ((I) -1) || n >= N) {
                // Invalid node:
                return hypernode<I>(-1, 0);
            } else {
                I index = parent.index ? ind2ptr_nonleaf(parent.depth, parent.index)->key.x[n] : 0;
                // A child has depth one less than that of its parent:
                return hypernode<I>(index, parent.depth - 1);
            }
        }

        template<bool DeleteUnmarked>
        void gc_traverse(uint32_t mindepth) {
            /*
            * Run gc_traverse<true> to delete all items with zeroed gcflags.
            * Regardless, this function zeroes all (remaining) elements' gcflags.
            */
            for (unsigned int i = 0; i < nonleaves.size(); i++) {
                if (i + 1 >= mindepth) {
                    nonleaves[i]->template gc_traverse<DeleteUnmarked>();
                }
            }
            if (mindepth == 0) { leaves.template gc_traverse<DeleteUnmarked>(); }
        }

        // Recursively mark node to rescue it from garbage-collection:
        I gc_mark(uint32_t mindepth, hypernode<I> parent) {

            if (parent.depth < mindepth) { return 0; }

            if (parent.index2 != 0) {
                gc_mark(mindepth, hypernode<I>(parent.index2, parent.depth));
                gc_mark(mindepth, hypernode<I>(parent.index, parent.depth));
                return 0;
            } else if (parent.index == 0 || parent.index == ((I) -1)) {
                return 0;
            } else if (parent.depth == 0) {
                kiventry<LK, I, LV>* pptr = leaves.ind2ptr(parent.index);
                if (pptr->gcflags == 0) {
                    // if (outfile) {(*outfile) << 'L' << ':' << pptr->key.toBase85() << '\n';}
                    pptr->gcflags = (++leaves.gccounter);
                }
                return pptr->gcflags;
            } else {
                kiventry<nicearray<I, N>, I, NV>* pptr = ind2ptr_nonleaf(parent.depth, parent.index);
                if (pptr->gcflags == 0) {
                    nicearray<I, N> children;
                    for (int i = 0; i < N; i++) {
                        children.x[i] = gc_mark(mindepth, hypernode<I>(pptr->key.x[i], parent.depth-1));
                    }
                    // if (outfile) {(*outfile) << 'N' << parent.depth << ':' << children.toBase85() << '\n';}
                    pptr->gcflags = (++(nonleaves[parent.depth-1]->gccounter));
                }
                return pptr->gcflags;
            }
        }

        void gc_full(uint32_t mindepth) {

            uint64_t origbytes = total_bytes();

            if (origbytes > 1000000000) {
                std::cerr << "Applying garbage collection from level " << mindepth << " upwards:" << std::endl;
                std::cerr << " -- emptying tree..." << std::endl;
            }

            gc_traverse<false>(mindepth);

            if (origbytes > 1000000000) {
                std::cerr << " -- marking important nodes..." << std::endl;
            }

            for (auto kv : handles) {
                gc_mark(mindepth, kv.second);
            }
            for (auto kv : ihandles) {
                gc_mark(mindepth, kv.second);
            }

            if (origbytes > 1000000000) {
                std::cerr << " -- removing surplus nodes..." << std::endl;
            }

            gc_traverse<true>(mindepth);

            if (origbytes > 1000000000) {
                uint64_t newbytes = total_bytes();
                std::cerr << " -- completed." << std::endl;
                std::cerr << "Hypertree memory reduced from " << origbytes << " to " << newbytes << " bytes." << std::endl;
            }

        }

        void gc_full() { gc_full(0); }

        bool gc_partial() {

            I maxnodes = (std::numeric_limits<I>::max() >> 3) * 7;

            if (leaves.size() > maxnodes) { gc_full(0); return true; }

            for (uint32_t i = 0; i < nonleaves.size(); i++) {
                if (nonleaves[i]->size() > maxnodes) { gc_full(i + 1); return true; }
            }

            return false;

        }

        I make_leaf(LK contents) {
            return leaves.getnode(contents, true);
        }

        I make_nonleaf(uint32_t depth, nicearray<I, N> indices) {
            while (nonleaves.size() < depth) {
                // std::cout << "Adding layer " << (nonleaves.size() + 1) << "..." << std::endl;
                // TODO: Use C++14 std::make_unique
                nonleaves.emplace_back(new kivtable<nicearray<I, N>, I, NV>);
                // std::cout << "...done!" << std::endl;
            }
            // std::cout << depth << std::endl;
            return nonleaves[depth-1]->getnode(indices, true);
        }

        hypernode<I> make_nonleaf_hn(uint32_t depth, nicearray<I, N> indices) {
            return hypernode<I>(make_nonleaf(depth, indices), depth);
        }

        explicit hypertree() = default;

    };

}

