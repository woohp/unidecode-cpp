import glob
import importlib.util
import os
from jinja2 import Template


def repr_single(s):
    return "'" + repr('"' + s)[2:]


def repr_double(s):
    single = repr_single(s)
    return '"' + single[1:-1].replace('"', '\\"').replace('\\\'', '\'') + '"'


template_ = '''
#include <array>
#include <string>
#include <string_view>

inline std::string unidecode(const std::u32string& input)
{
    using namespace std;

    {% for bucket_name, data in buckets -%}
    constexpr static std::array<std::string_view, {{ data|length }}> {{ bucket_name }}_data = {% raw %}{{% endraw %}
    {{ data|join(',') }}
    {% raw %}};{% endraw %}
    {% endfor -%}

    std::string output;
    output.reserve(input.length());

    for (const auto codepoint : input)
    {
        if (codepoint < 0x80)  // ASCII
        {
            output += codepoint;
            continue;
        }

        if (codepoint > 0xeffff)
            continue;

        const auto bucket = codepoint >> 8;
        const auto position = codepoint % 256;

        switch (bucket)
        {
        {% for bucket_name, _ in buckets -%}
        case 0{{ bucket_name }}: if (position < {{ bucket_name }}_data.size()) output += {{ bucket_name }}_data[position]; break;
        {% endfor -%}
        }
    }

    return output;
}
'''


def main():
    files = sorted(glob.glob('unidecode/unidecode/x*.py'))
    buckets = []

    for filename in files:
        bucket_name = os.path.splitext(os.path.basename(filename))[0]
        spec = importlib.util.spec_from_file_location("module.name", filename)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        data = foo.data
        data = [repr_double(c) + 'sv' for c in data]
        buckets.append((bucket_name, data))

    template = Template(template_)
    with open('unidecode.hpp', 'w') as f:
        print(template.render(buckets=buckets), file=f)


if __name__ == '__main__':
    main()
