def parse_instrumentation(instrumentation_input):
    with open("instrumentation_list.txt") as f:
        data = f.readlines()
        instrumentation = []
        for each in instrumentation_input.split(","):
            try:
                # Tries to append instruments by index
                instrumentation.append(data[int(each)].strip())
            except:
                # Append instruments by index with "#" modifier
                if each[0] == "#":
                    instrumentation.append(f"#{data[int(each[1:])].strip()}")
                # Parses common instrument ensembles
                elif each[0] == "!":
                    if each[1:] == "Strings":
                        instrumentation.extend(["Violin","Violin","Viola","Violoncello","Double Bass"])
                    elif each[1:] == "SATB":
                        instrumentation.extend(["Soprano","Alto","Tenor","Bass"])
                # Append instruments directly
                else:
                    instrumentation.append(each)
        return instrumentation

test = input()
if not test:
    test = None

print(type(test))
