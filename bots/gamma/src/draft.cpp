#include <cambc.h>
#include "draft.h"
#include "plan.h"
#include <algorithm>
#include <array>
#include <vector>

void play_draft() {
    namespace bc = cambc;
    using D = bc::champion_draft;
    const auto chosen = bc::draft::current_draft(bc::team::ally);
    if (chosen.size() >= bc::draft::team_size()) return;
    if (chosen.empty()) {
        // Spend the large FIRST draft budget on layout, rather than loading the
        // whole map separately in every champion's 100k-fuel gameplay turn.
        const auto home = bc::map::spawn_region(bc::team::ally).positions().front();
        struct Anchor { bc::vec2 position; bool has_gems; };
        std::vector<Anchor> anchors;
        for (const auto& g : bc::map::camp_groups())
            anchors.push_back({g.camps().front().spawn_position(), g.gem_value() > 0});
        std::stable_sort(anchors.begin(), anchors.end(), [&](auto a, auto b) {
            return home.chebyshev_distance(a.position) < home.chebyshev_distance(b.position);
        });
        const auto n = std::min(anchors.size(), policy::max_groups);
        const bool with_rewards = policy::reward_mask_fits(n);
        std::vector<std::uint8_t> bytes(with_rewards ? policy::reward_plan_size(n) : policy::plan_header + 2*n);
        bytes[0] = 'G'; bytes[1] = 'A'; bytes[2] = 2;
        bytes[3] = n & 255; bytes[4] = n >> 8;
        for (std::size_t i = 0; i < n; ++i) {
            bytes[5+2*i] = anchors[i].position.x; bytes[6+2*i] = anchors[i].position.y;
            if (with_rewards && anchors[i].has_gems)
                bytes[policy::reward_offset(n,i)] |= policy::reward_bit(i);
        }
        bc::draft_memory = bytes;
    }
    // Independent melee farmers retain walking + attacking. Varg specializes
    // in dense camps; Vendetta in finishes; Ryth/Marcella supply control.
    constexpr std::array order{D::varg, D::vendetta, D::ryth, D::marcella,
        D::heart_of_ruin, D::tavi, D::vesper_vale, D::ren, D::stellar,
        D::prism, D::willow, D::cassi_and_issac};
    for (auto pick : order)
        if (std::find(chosen.begin(), chosen.end(), pick) == chosen.end()) {
            bc::draft::pick(pick);
            return;
        }
}
