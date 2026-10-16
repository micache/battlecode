// A controlled hidden-obstruction probe, not a scoring bot.
#include <cambc.h>
#include "role.h"
#include <algorithm>
#include <iostream>
#include <optional>

int main() {
    bool tested=false;
    std::optional<cambc::vec2> target;
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
                        for (auto tile:cambc::map::bushes().positions())
                            if (!forbidden.is_set(tile) && (!target || tile.chebyshev_distance(center)<target->chebyshev_distance(center))) target=tile;
                        if (target) std::cout << "HIDDEN target=" << target->x << ',' << target->y << std::endl;
                    }
                    if (target && me.position()!=*target && me.can_move()) {
                        const bool known=cambc::vision::champion_tiles(cambc::team::enemy).is_set(*target);
                        const bool moved=me.move_towards(*target);
                        if (!blocker && !moved && !known && me.can_move() &&
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
                            tested=true;
                        }
                    }
                }
            }
        } catch (const std::exception& e) { std::cout << "CHECK FAIL exception " << e.what() << std::endl; }
        cambc::end_turn();
    }
}
