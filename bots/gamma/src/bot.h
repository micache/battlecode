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
    };
    bool initialized = false;
    bool recovering = false;
    int target = -1, slot = 0, now = 0, cursor = 0;
    int last_log = -100, stuck = 0;
    std::vector<Route> routes;
    cambc::bitboard terrain, spawn, altar_goals;
    std::vector<cambc::vec2> altars;
    void initialize();
    void buy_items();
    bool walk(cambc::bitboard goals, bool dash = false);
    bool threatened(cambc::vec2 p);
    bool bank();
    bool fight(bool moved, bool champions_only = false);
    void shield();
    void recover();
    void farm();
    bool load_route(int index);
    void observe(int index, const cambc::bitboard& visible);
    void log(const char* mode);
public:
    void play_turn();
};
