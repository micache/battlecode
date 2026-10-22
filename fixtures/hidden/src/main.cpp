// A controlled hidden-obstruction probe, not a scoring bot.
#include <cambc.h>
#include "role.h"
#include <algorithm>
#include <iostream>
#include <optional>

int main() {
    bool tested=false;
    std::optional<cambc::vec2> target, approach;
    for (;;) {
        try {
            if (cambc::is_draft()) {
                auto chosen=cambc::draft::current_draft(cambc::team::ally);
                for (int i=0;i<3;++i) {
                    auto pick=cambc::champion_draft(i);
                    if (std::find(chosen.begin(),chosen.end(),pick)==chosen.end()) {
                        cambc::draft::pick(pick);break;
                    }
                }
            } else {
                auto& me=cambc::self();
                if (me.is_alive() && int(me.champion_name())==0 && !tested && (blocker || cambc::round_number()>=150)) {
                    if (!target) {
                        auto forbidden=cambc::map::walls() | cambc::map::holes() | cambc::map::altars() |
                            cambc::map::spawn_region(cambc::team::ally) | cambc::map::spawn_region(cambc::team::enemy);
                        for (auto group:cambc::map::camp_groups()) forbidden |= group.spawn_tiles();
                        const auto center=cambc::vec2{cambc::map::width()/2,cambc::map::height()/2};
                        const auto bushes=cambc::map::bushes();
                        for (auto tile:bushes.positions()) {
                            if (forbidden.is_set(tile)) continue;
                            for (int dx=-1;dx<=1;++dx) for (int dy=-1;dy<=1;++dy) {
                                const auto outside=tile+cambc::vec2{dx,dy};
                                if (!(dx||dy) || !cambc::map::is_in_bounds(outside) ||
                                    forbidden.is_set(outside) || bushes.is_set(outside)) continue;
                                if (!target || tile.chebyshev_distance(center)<target->chebyshev_distance(center)) {
                                    target=tile;approach=outside;
                                }
                            }
                        }
                        if (target) std::cout << "HIDDEN target=" << target->x << ',' << target->y
                            << " approach=" << approach->x << ',' << approach->y << std::endl;
                    }
                    if (target && blocker && me.position()!=*target && me.can_move()) {
                        me.move_towards(*target);
                    } else if (target && !blocker && me.can_move()) {
                        // Never enter the connected bush while approaching: that would
                        // reveal the occupant before the supposedly hidden step.
                        if (me.position()!=*approach) {
                            auto blocked=cambc::map::walls() | cambc::map::holes() | cambc::map::altars() |
                                cambc::map::bushes() | cambc::map::spawn_region(cambc::team::enemy) |
                                cambc::vision::champion_tiles() | cambc::vision::camp_tiles();
                            for (auto group:cambc::map::camp_groups()) blocked |= group.spawn_tiles();
                            blocked.set(me.position(),false);
                            cambc::bitboard roots,visited;
                            roots.set(*approach,true);
                            cambc::distance_field distances;
                            distances.compute(blocked,roots,visited);
                            const auto step=distances.next_move_from(me.position());
                            if (step) me.move(*step);
                            cambc::end_turn();
                            continue;
                        }
                        const bool known=cambc::vision::champion_tiles(cambc::team::enemy).is_set(*target);
                        if (known) {
                            std::cout << "CHECK FAIL hidden-fixture-precondition-known\n";
                            tested=true;
                            cambc::end_turn();
                            continue;
                        }
                        const bool moved=me.move_absolute(*target);
                        std::cout << "HIDDEN trace round=" << cambc::round_number() << " position=" << me.position().x
                                  << ',' << me.position().y << " known=" << known << " moved=" << moved << std::endl;
                        if (!moved && me.can_move() &&
                            cambc::vision::champion_tiles(cambc::team::enemy).is_set(*target)) {
                            std::cout << "CHECK PASS hidden-obstruction-preserves-move round=" << cambc::round_number() << std::endl;
                            try { me.move_absolute(*target); std::cout << "CHECK FAIL known-obstruction-did-not-throw\n"; }
                            catch (const cambc::error&) { std::cout << "CHECK PASS known-obstruction-throws\n"; }
                            auto occupied=cambc::vision::champion_tiles() | cambc::vision::camp_tiles() |
                                cambc::map::walls() | cambc::map::holes() | cambc::map::altars() |
                                cambc::map::spawn_region(cambc::team::enemy);
                            bool recovered=false;
                            auto origin=me.position();
                            for (int dx=-1;dx<=1 && !recovered;++dx) for (int dy=-1;dy<=1 && !recovered;++dy) {
                                auto tile=origin+cambc::vec2{dx,dy};
                                if ((dx||dy) && cambc::map::is_in_bounds(tile) && !occupied.is_set(tile)) recovered=me.move_absolute(tile);
                            }
                            std::cout << "CHECK " << (recovered?"PASS":"FAIL") << " hidden-legal-fallback" << std::endl;
                        } else std::cout << "CHECK FAIL hidden-obstruction-not-observed\n";
                        tested=true;
                    }
                }
            }
        } catch (const std::exception& e) { std::cout << "CHECK FAIL exception " << e.what() << std::endl; }
        cambc::end_turn();
    }
}
