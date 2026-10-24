#pragma once
#include <cambc.h>
#include <optional>
#include <vector>

class Bot {
    struct Route {
        cambc::vec2 anchor;
        std::optional<cambc::map::camp_group> group;
        int ready_at = 0, observed_at = -1, state = 0;
        float hp = 0, strength = 0;
        int travel = -1; // Static distance observation from travel_origin.
    };
    bool initialized = false;
    bool recovering = false;
    int target = -1, slot = 0, now = 0, cursor = 0;
    int last_log = -100, stuck = 0;
    int bank_best = 1000000, bank_progress_at = -1;
    std::vector<Route> routes;
    cambc::bitboard terrain, spawn, altar_goals;
    std::vector<cambc::vec2> altars;
    std::optional<cambc::distance_field> altar_field;
    std::optional<cambc::distance_field> travel_field;
    cambc::vec2 travel_position{};
    int travel_displacement = 0;
    int travel_round = -1;
    void refresh_travel();
    int route_distance(int index) const;
    void initialize();
    void buy_items();
    bool walk(cambc::bitboard goals, bool dash = false);
    bool threatened(cambc::vec2 p);
    bool bank();
    bool clear_bank_path();
    bool fight(bool moved, bool champions_only = false,
        const std::optional<cambc::camp>& obstacle = std::nullopt);
    void shield();
    void recover();
    void farm();
    bool load_route(int index);
    void observe(int index, const cambc::bitboard& visible);
    void log(const char* mode);
public:
    void play_turn();
};
