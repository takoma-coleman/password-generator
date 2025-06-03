#include <iostream>
#include <string>
#include <random>
#include <ctime>

// Move RNG and distribution to global scope or pass them in
std::mt19937 rng(static_cast<unsigned int>(time(0)));

std::string generate_password(int length, bool use_numbers, bool use_specials) {
    std::string letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    std::string numbers = "0123456789";
    std::string specials = "!@#$%^&*()-_=+[]{};:,.<>?/|";
    
    std::string character_pool = letters;
    if (use_numbers) character_pool += numbers;
    if (use_specials) character_pool += specials;

    if (character_pool.empty()) return "Error: No character pool selected.";

    std::string password;
    std::uniform_int_distribution<> dist(0, character_pool.size() - 1);

    for (int i = 0; i < length; ++i) {
        password += character_pool[dist(rng)];
    }

    return password;
}

int main() {
    int length, count;
    char include_numbers, include_specials;

    std::cout << "Password length: ";
    std::cin >> length;

    std::cout << "Include numbers? (y/n): ";
    std::cin >> include_numbers;

    std::cout << "Include special characters? (y/n): ";
    std::cin >> include_specials;

    std::cout << "How many passwords to generate? (default 1): ";
    std::cin >> count;

    bool use_numbers = (include_numbers == 'y' || include_numbers == 'Y');
    bool use_specials = (include_specials == 'y' || include_specials == 'Y');

    std::cout << "\nGenerated Password(s):\n";
    for (int i = 0; i < count; ++i) {
        std::cout << generate_password(length, use_numbers, use_specials) << "\n";
    }

    return 0;
}
