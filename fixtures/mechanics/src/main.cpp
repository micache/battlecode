// Non-scoring SDK observer around the pinned official starter's Bot class.
#include <cambc.h>
#include "bot.h"
#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>
#include <variant>

void check(bool ok, const char* name) {
    std::cout << "CHECK " << (ok ? "PASS " : "FAIL ") << name
              << " round=" << cambc::round_number() << std::endl;
}

int main() {
    Bot bot;
    int recall_start=-1, previous_round=-1, previous_tribute=-1;
    unsigned previous_gems=0;
    int capture_group=-1, capture_start=-1;
    unsigned capture_gems=0;
    bool recall_done=false, approach_checked=false, captured=false, range_checked=false;
    for (;;) {
        try {
            if (cambc::is_draft()) {
                const std::array picks{cambc::champion_draft(0),cambc::champion_draft(6),cambc::champion_draft(5)};
                const auto chosen=cambc::draft::current_draft(cambc::team::ally);
                for (auto pick:picks) if (std::find(chosen.begin(),chosen.end(),pick)==chosen.end()) {
                    cambc::draft::pick(pick); break;
                }
            } else {
                auto& me=cambc::self();
                const int round=cambc::round_number();
                if (!me.is_alive()) { previous_tribute=-1; capture_start=-1; }
                else if (!recall_done) {
                    if (recall_start<0) {
                        me.recall(); recall_start=round;
                        check(me.is_recalling() && me.remaining_channel_time()==5,"recall-start-five");
                    } else if (round-recall_start<5) {
                        check(me.is_recalling() && me.remaining_channel_time()==5-(round-recall_start),"recall-countdown");
                    } else {
                        check(round-recall_start==5 && !me.is_recalling() &&
                              cambc::map::spawn_region(cambc::team::ally).is_set(me.position()),"channel-completion");
                        recall_done=true;
                    }
                } else if (round>=200 || int(me.champion_name())==0) {
                    if (previous_round==round-1 && previous_tribute==1 && !me.is_submitting_gems() &&
                        previous_gems>0 && me.gem_count()==0)
                        check(true,"tribute-completion-next-start");
                    if (capture_start>=0) {
                        bool still_here=false;
                        for (const auto& group:cambc::vision::camp_groups())
                            if (int(cambc::handle_camp_group_t(group))==capture_group) {
                                still_here=group.spawn_tiles().is_set(me.position());
                                if (std::holds_alternative<cambc::map::camp_group_respawning>(group.state()) &&
                                    me.gem_count()>capture_gems) {
                                    check(round-capture_start>=6,"capture-occupancy-five-later-phases");
                                    captured=true; capture_start=-1;
                                }
                            }
                        if (!still_here) capture_start=-1;
                    }
                    if (!approach_checked && me.can_move() && !cambc::map::altars().is_empty()) {
                        const auto old=me.position();
                        try {
                            const bool moved=me.move_towards(cambc::map::altars().positions().front());
                            check(!cambc::map::altars().is_set(me.position()) &&
                                  (moved || me.position()==old),"blocked-target-path-keeps-legal-landing");
                        } catch(const cambc::error&) {
                            check(me.position()==old && me.can_move(),"blocked-target-landing-rejected");
                        }
                        approach_checked=true;
                    }
                    const auto before=me.position();
                    const auto gems=me.gem_count();
                    const bool could_attack=me.can_attack(), could_move=me.can_move(), was_tribute=me.is_submitting_gems();
                    const int range=me.attack_range();
                    bot.play_turn();
                    if (cambc::round_number()==unsigned(round) && me.is_alive()) {
                        const bool channel=me.is_recalling() || me.is_submitting_gems() || me.is_teleporting();
                        if (!range_checked && range>1 && !channel && could_move && could_attack &&
                            (me.position()!=before || !me.can_attack())) {
                            check(!(me.can_move() || me.can_attack()),"ranged-shared-action-allowance");
                            range_checked=true;
                        }
                        if (gems>0 && before!=me.position())
                            check(!cambc::map::altars().is_set(me.position()),"safe-altar-approach");
                        if (!was_tribute && me.is_submitting_gems())
                            check(me.remaining_channel_time()==std::max(1,int(std::ceil(double(gems)/10))),"tribute-start-duration");
                        if (!captured && round<180 && int(me.champion_name())==0 && capture_start<0)
                            for (const auto& group:cambc::vision::camp_groups())
                                if (group.spawn_tiles().is_set(me.position()) &&
                                    std::holds_alternative<cambc::map::camp_group_reward_available>(group.state())) {
                                    capture_group=int(cambc::handle_camp_group_t(group));
                                    capture_start=round; capture_gems=me.gem_count();
                                    std::cout << "CAPTURE entered round=" << round << " group=" << capture_group << std::endl;
                                    break;
                                }
                        previous_round=round;
                        previous_tribute=me.is_submitting_gems() ? me.remaining_channel_time() : -1;
                        previous_gems=me.gem_count();
                    }
                }
            }
        } catch (const std::exception& e) {
            std::cout << "CHECK FAIL exception " << e.what() << std::endl;
        }
        cambc::end_turn();
    }
}
