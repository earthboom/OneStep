#include <algorithm>
#include <charconv>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <optional>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
namespace fs = std::filesystem;

struct Encounter {
    std::string name;
    std::string board;
    int playerHp;
    int enemyHp;
    int playerDamage;
    int enemyDamage;
};

using Catalog = std::map<std::string, Encounter>;

std::string Trim(const std::string& text) {
    const auto first = text.find_first_not_of(" \t\r");
    const auto last = text.find_last_not_of(" \t\r");
    return first == std::string::npos ? "" : text.substr(first, last - first + 1);
}

bool IsId(const std::string& id) {
    const auto lowercase = [](char c) { return c >= 'a' && c <= 'z'; };
    return !id.empty() && id.size() <= 24 && lowercase(id.front()) &&
        std::all_of(id.begin(), id.end(), [&](char c) {
            return lowercase(c) || (c >= '0' && c <= '9') || c == '-';
        });
}

int ReadStat(const std::string& key, const std::string& value) {
    int number = 0;
    const auto end = value.data() + value.size();
    const auto result = std::from_chars(value.data(), end, number);
    if (result.ec != std::errc{} || result.ptr != end || number < 1 || number > 20) {
        throw std::runtime_error(key + " must be an integer from 1 to 20");
    }
    return number;
}

Encounter ReadEncounter(const fs::path& path) {
    if (!fs::is_regular_file(path)) {
        throw std::runtime_error("expected a regular encounter file");
    }
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("cannot open encounter");
    }

    std::map<std::string, std::string> fields{
        {"name", ""}, {"board", ""}, {"player_hp", ""}, {"enemy_hp", ""},
        {"player_damage", ""}, {"enemy_damage", ""},
    };
    std::size_t lineNumber = 0;
    for (std::string line; std::getline(input, line);) {
        ++lineNumber;
        line = Trim(line);
        if (line.empty() || line.front() == '#') {
            continue;
        }
        const auto invalid = [&](const std::string& reason) {
            return std::runtime_error("line " + std::to_string(lineNumber) + " " + reason);
        };
        const auto equals = line.find('=');
        if (equals == std::string::npos) {
            throw invalid("expected key=value");
        }
        const auto key = Trim(line.substr(0, equals));
        const auto field = fields.find(key);
        if (field == fields.end()) {
            throw invalid("unknown field " + key);
        }
        if (!field->second.empty()) {
            throw invalid("duplicate field " + key);
        }
        field->second = Trim(line.substr(equals + 1));
        if (field->second.empty()) {
            throw invalid("empty field " + key);
        }
    }
    if (input.bad()) {
        throw std::runtime_error("cannot read encounter");
    }
    for (const auto& field : fields) {
        if (field.second.empty()) {
            throw std::runtime_error("missing field " + field.first);
        }
    }

    const auto& name = fields.at("name");
    if (name.size() > 48 ||
        !std::all_of(name.begin(), name.end(), [](char c) { return c >= ' ' && c <= '~'; })) {
        throw std::runtime_error("name must contain 1 to 48 printable ASCII characters");
    }
    const auto& board = fields.at("board");
    if (board.size() < 4 || board.size() > 12 ||
        board.find_first_not_of(".PE") != std::string::npos ||
        std::count(board.begin(), board.end(), 'P') != 1 ||
        std::count(board.begin(), board.end(), 'E') != 1) {
        throw std::runtime_error("board must have 4 to 12 cells with one P and one E");
    }
    return {
        name, board, ReadStat("player_hp", fields.at("player_hp")),
        ReadStat("enemy_hp", fields.at("enemy_hp")),
        ReadStat("player_damage", fields.at("player_damage")),
        ReadStat("enemy_damage", fields.at("enemy_damage")),
    };
}

Catalog LoadCatalog(const fs::path& directory) {
    Catalog catalog{{"core", {"Crossing", "P...E", 6, 3, 2, 2}}};
    if (!fs::exists(directory)) {
        return catalog;
    }
    std::vector<fs::path> paths;
    for (const auto& entry : fs::directory_iterator(directory)) {
        if (entry.path().extension() == ".enc") {
            paths.push_back(entry.path());
        }
    }
    std::sort(paths.begin(), paths.end());
    for (const auto& path : paths) {
        try {
            const auto id = path.stem().string();
            if (!IsId(id) || catalog.count(id) != 0) {
                throw std::runtime_error("invalid or reserved encounter ID");
            }
            catalog.emplace(id, ReadEncounter(path));
        } catch (const std::exception& error) {
            throw std::runtime_error(path.filename().string() + ": " + error.what());
        }
    }
    return catalog;
}

enum class Action { MoveLeft, MoveRight, Strike, Guard };

class Session {
public:
    explicit Session(const Encounter& encounter)
        : encounter_(encounter),
          player_(static_cast<int>(encounter.board.find('P'))),
          enemy_(static_cast<int>(encounter.board.find('E'))),
          playerHp_(encounter.playerHp),
          enemyHp_(encounter.enemyHp) {}

    void PrintState() const {
        std::string board(encounter_.board.size(), '.');
        if (playerHp_ > 0) {
            board[static_cast<std::size_t>(player_)] = 'P';
        }
        if (enemyHp_ > 0) {
            board[static_cast<std::size_t>(enemy_)] = 'E';
        }
        std::cout << "State turn=" << turn_ << " board=" << board
                  << " player_hp=" << playerHp_ << " enemy_hp=" << enemyHp_ << '\n';
    }

    std::string TryAction(Action action) {
        if (playerHp_ == 0 || enemyHp_ == 0) {
            return "encounter is over. Use start to play again.";
        }
        const auto rejection = ApplyPlayerAction(action);
        if (!rejection.empty()) {
            return rejection;
        }
        ++turn_;
        Respond(action == Action::Guard);
        if (playerHp_ == 0) {
            std::cout << "Result defeat.\n";
        } else if (enemyHp_ == 0) {
            std::cout << "Result victory.\n";
        }
        PrintState();
        return {};
    }

private:
    bool Adjacent() const {
        return player_ == enemy_ - 1 || player_ == enemy_ + 1;
    }

    std::string ApplyPlayerAction(Action action) {
        switch (action) {
        case Action::MoveLeft:
        case Action::MoveRight: {
            const bool right = action == Action::MoveRight;
            const int next = player_ + (right ? 1 : -1);
            if (next < 0 || next >= static_cast<int>(encounter_.board.size()) || next == enemy_) {
                return "player cannot move there.";
            }
            player_ = next;
            std::cout << "Player moves " << (right ? "right" : "left") << ".\n";
            return {};
        }
        case Action::Strike:
            if (!Adjacent()) {
                return "player cannot strike at this distance.";
            }
            enemyHp_ = std::max(0, enemyHp_ - encounter_.playerDamage);
            std::cout << "Player deals " << encounter_.playerDamage << " damage.\n";
            return {};
        case Action::Guard:
            std::cout << "Player guards.\n";
            return {};
        }
        throw std::logic_error("invalid action");
    }

    void Respond(bool guarding) {
        if (enemyHp_ == 0) {
            std::cout << "Enemy is defeated and cannot act.\n";
        } else if (!Adjacent()) {
            enemy_ += player_ < enemy_ ? -1 : 1;
            std::cout << "Enemy closes in.\n";
        } else {
            const int damage = guarding ? std::max(0, encounter_.enemyDamage - 2) : encounter_.enemyDamage;
            playerHp_ = std::max(0, playerHp_ - damage);
            std::cout << "Enemy deals " << damage << " damage.";
            if (guarding && playerHp_ > 0) {
                --enemyHp_;
                std::cout << " Guard counters for 1.";
            }
            std::cout << '\n';
        }
    }

    const Encounter& encounter_;
    int player_;
    int enemy_;
    int playerHp_;
    int enemyHp_;
    std::uint64_t turn_ = 0;
};

void PrintHelp() {
    std::cout << "Commands: list, start ID, status, move left, move right, strike, guard, help, quit\n"
              << "Move one cell, strike an adjacent enemy, or guard to absorb up to 2 damage "
                 "and counter an adjacent attack if you survive.\n";
}

void Run(const Catalog& catalog) {
    std::optional<Session> session;
    const auto reject = [&](const std::string& reason) {
        std::cout << "Rejected " << reason << '\n';
        if (session) {
            session->PrintState();
        }
    };

    std::cout << "Crossing Tactics\n";
    PrintHelp();
    for (std::string line; std::getline(std::cin, line);) {
        std::istringstream input(line);
        std::string command, argument, extra;
        input >> command >> argument >> extra;
        const bool needsArgument = command == "start" || command == "move";
        if (!extra.empty() || needsArgument != !argument.empty()) {
            reject("invalid arguments. Type help for commands.");
            continue;
        }
        if (command == "quit") {
            return;
        }
        if (command == "help") {
            PrintHelp();
        } else if (command == "list") {
            for (const auto& item : catalog) {
                std::cout << "Encounter " << item.first << " | " << item.second.name << '\n';
            }
        } else if (command == "start") {
            const auto found = catalog.find(argument);
            if (found == catalog.end()) {
                reject("unknown encounter " + argument + ".");
                continue;
            }
            session.emplace(found->second);
            std::cout << "Started " << found->second.name << ".\n";
            session->PrintState();
        } else if (command == "status") {
            if (session) {
                session->PrintState();
            } else {
                reject("start an encounter first.");
            }
        } else {
            std::optional<Action> action;
            if (command == "move" && argument == "left") {
                action = Action::MoveLeft;
            } else if (command == "move" && argument == "right") {
                action = Action::MoveRight;
            } else if (command == "strike") {
                action = Action::Strike;
            } else if (command == "guard") {
                action = Action::Guard;
            }
            if (!action) {
                reject("unknown command or direction. Type help for commands.");
            } else if (!session) {
                reject("start an encounter first.");
            } else {
                const auto reason = session->TryAction(*action);
                if (!reason.empty()) {
                    reject(reason);
                }
            }
        }
    }
}
}

int main(int argc, char** argv) {
    if (argc > 2) {
        std::cerr << "Usage: tactics [pack-directory]\n";
        return 2;
    }
    try {
        const auto catalog = LoadCatalog(argc == 2 ? argv[1] : "packs");
        Run(catalog);
    } catch (const std::exception& error) {
        std::cerr << "Error loading encounters: " << error.what() << '\n';
        return 2;
    }
    return 0;
}
