from re_setup import testing_RE_md

with testing_RE_md(RE):
    print("This sample dictionary should be referencing testing.")
    print(get_sample_dict())

print("This sample dictionary should be referencing the most recent sample.")
print(get_sample_dict())
