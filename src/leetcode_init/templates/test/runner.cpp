#include CASE_HEADER

#include <cstdio>
#include <iostream>
#include <streambuf>
#include <string>
#include <string_view>

#include "{{problem}}.hpp"

namespace {
constexpr std::string_view case_input{CASE_INPUT};
constexpr std::string_view case_expected{CASE_EXPECTED};

class ViewBuf : public std::streambuf {
 public:
  explicit ViewBuf(std::string_view data) {
    auto* begin = const_cast<char*>(data.data());
    setg(begin, begin, begin + data.size());
  }
};

class StringBuf : public std::streambuf {
 public:
  std::string data;

 protected:
  int_type overflow(int_type ch) override {
    if (!traits_type::eq_int_type(ch, traits_type::eof())) {
      data.push_back(traits_type::to_char_type(ch));
    }
    return ch;
  }
  std::streamsize xsputn(const char* s, std::streamsize n) override {
    data.append(s, static_cast<std::size_t>(n));
    return n;
  }
};
}  // namespace

int main() {
  std::ios::sync_with_stdio(false);
  ViewBuf in{case_input};
  StringBuf out;
  out.data.reserve(case_expected.size());
  std::cin.rdbuf(&in);
  std::cout.rdbuf(&out);
  solve();
  std::cout.flush();
  if (out.data == case_expected) {
    return 0;
  }
  std::fprintf(stderr, "expected:\n%.*s\nactual:\n%.*s\n",
               static_cast<int>(case_expected.size()), case_expected.data(),
               static_cast<int>(out.data.size()), out.data.data());
  return 1;
}
