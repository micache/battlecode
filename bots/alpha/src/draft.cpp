#include <cambc.h>
#include "draft.h"
#include "draft_policy.h"
#include "equipment_model.h"
#include "random.h"
#include <array>
#include <string_view>

namespace {
constexpr std::array<cambc::champion_type, draft_policy::roster_size> first_body{
    cambc::champion_type::ryth, cambc::champion_type::vesper_vale,
    cambc::champion_type::vendetta, cambc::champion_type::cassi,
    cambc::champion_type::stellar, cambc::champion_type::prism,
    cambc::champion_type::marcella, cambc::champion_type::willow,
    cambc::champion_type::ren, cambc::champion_type::varg,
    cambc::champion_type::tavi, cambc::champion_type::heart_of_ruin};

float body_value(cambc::champion_type type, unsigned combine) {
    const auto& design = cambc::champion_designs[static_cast<unsigned>(type)];
    const auto stats = design.base_stats();
    const auto model = equipment_model::estimate(design,
        stats.base_health, stats.base_strength, stats.base_focus);
    return draft_policy::opening_value(model, combine);
}

std::array<float, draft_policy::roster_size> score_roster() {
    std::array<float, draft_policy::roster_size> values{};
    const auto combine = cambc::item_type::power_shard_of_strength.combine_count();
    for (unsigned pick = 0; pick < values.size(); ++pick) {
        values[pick] = body_value(first_body[pick], combine);
        if (static_cast<cambc::champion_draft>(pick) == cambc::champion_draft::cassi_and_issac) {
            values[pick] += body_value(cambc::champion_type::issac, combine);
            // Two farmers, but either body's death removes both. This fixed
            // exposure discount is a policy assumption, not a measured rate.
            values[pick] *= draft_policy::linked_survival_credit;
        }
    }
    return values;
}
} // namespace

void play_draft() {
    const auto chosen = cambc::draft::current_draft(cambc::team::ally);
    if (chosen.size() >= cambc::draft::team_size()) return;
    // First draft turn has the enlarged budget. Later turns only select from
    // twelve cached immutable scores; no map/camp scans or hidden-unit queries.
    static const auto values = score_roster();
    std::array<bool, draft_policy::roster_size> taken{};
    for (const auto pick : chosen) {
        const auto index = static_cast<unsigned>(pick);
        if (index < taken.size()) taken[index] = true;
    }
    const auto pick = draft_policy::select(values, taken, random_number(taken.size()));
    if (pick >= taken.size()) return; // only possible once all twelve are taken
    cambc::draft_memory = std::string_view("hello world");
    cambc::draft::pick(static_cast<cambc::champion_draft>(pick));
}
