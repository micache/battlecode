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
        auto groups = bc::map::camp_groups();
        const auto home = bc::map::spawn_region(bc::team::ally).positions().front();
        std::stable_sort(groups.begin(), groups.end(), [&](const auto& a, const auto& b) {
            return home.chebyshev_distance(a.camps().front().spawn_position())
                 < home.chebyshev_distance(b.camps().front().spawn_position());
        });
        const auto n = std::min(groups.size(), policy::max_groups);
        std::vector<std::uint8_t> bytes(policy::plan_header + 2*n);
        bytes[0] = 'G'; bytes[1] = 'A'; bytes[2] = 1;
        bytes[3] = n & 255; bytes[4] = n >> 8;
        for (std::size_t i = 0; i < n; ++i) {
            const auto p = groups[i].camps().front().spawn_position();
            bytes[5+2*i] = p.x; bytes[6+2*i] = p.y;
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
