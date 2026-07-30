#include "{{problem}}.hpp"

#include CASE_HEADER

#include <cstdlib>
#include <iostream>
#include <streambuf>
#include <string>
#include <string_view>

namespace {
class ViewBuf : public std::streambuf
{
public:
  explicit ViewBuf(
    std::string_view data)
  {
    // NOLINTBEGIN(*-type-const-cast,*-bounds-pointer-arithmetic)
    auto* begin = const_cast<char*>(data.data());
    setg(begin, begin, begin + data.size());
    // NOLINTEND(*-type-const-cast,*-bounds-pointer-arithmetic)
  }
};

class RdbufGuard
{
  std::ios*       mStream;
  std::streambuf* mOld;

public:
  RdbufGuard(
    std::ios*       stream,
    std::streambuf* buffer)
    : mStream{ stream }
    , mOld{ stream->rdbuf(buffer) }
  {
  }

  RdbufGuard(RdbufGuard&&)                 = default;
  RdbufGuard(RdbufGuard const&)            = delete;
  RdbufGuard& operator=(RdbufGuard&&)      = delete;
  RdbufGuard& operator=(RdbufGuard const&) = delete;

  ~RdbufGuard()
  {
    mStream->rdbuf(mOld);
  }
};

class StringBuf : public std::streambuf
{
public:
  std::string mData;

protected:
  auto overflow(
    int_type symbol) -> int_type override
  {
    if (!traits_type::eq_int_type(symbol, traits_type::eof())) {
      mData.push_back(traits_type::to_char_type(symbol));
    }
    return symbol;
  }

  auto xsputn(
    char const*     rawString,
    std::streamsize rawStringSize) -> std::streamsize override
  {
    mData.append(rawString, static_cast<std::size_t>(rawStringSize));
    return rawStringSize;
  }
};
} // namespace

int
main()
{
  std::ios::sync_with_stdio(false);

  auto oBuf = StringBuf{};
  oBuf.mData.reserve(test::gCaseExpected.size());

  {
    auto iBuf  = ViewBuf{ test::gCaseInput };
    auto iSwap = RdbufGuard{ &std::cin, &iBuf };
    auto oSwap = RdbufGuard{ &std::cout, &oBuf };

    solve();
    std::cout.flush();
  }

  if (oBuf.mData == test::gCaseExpected) {
    std::cout << oBuf.mData << '\n';
    std::cout.flush();
    return EXIT_SUCCESS;
  }

  std::cerr << "expected:\n" << test::gCaseExpected << '\n';
  std::cerr << "actual:\n" << oBuf.mData << '\n';
  std::cerr.flush();
  return EXIT_FAILURE;
}
