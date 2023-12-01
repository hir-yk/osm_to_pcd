import sys
import xml.etree.ElementTree as ET


def process_node(node):
    local_x = None
    local_y = None
    ele = None
        
    for child in node:
        if child.attrib["k"] == "local_x":
            local_x = child.attrib["v"]
        elif child.attrib["k"] == "local_y":
            local_y = child.attrib["v"]
        elif child.attrib["k"] == "ele":
            ele = child.attrib["v"]
        
    if local_x and local_y and ele:
        return f"{local_x} {local_y} {ele} 127\n"


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 this_script.py <filepath>")
        sys.exit(1)

    osm_file_path = sys.argv[1]
    tree = ET.parse(osm_file_path)
    root = tree.getroot()

    lines = [process_node(node) for node in root.findall("node")]
    lines = list(filter(None, lines))  # Remove None items

    with open("output.pcd", "w") as output_file:
        output_file.write("# .PCD v0.7 - Point Cloud Data file format\n")
        output_file.write("VERSION 0.7\n")
        output_file.write("FIELDS x y z intensity\n")
        output_file.write("SIZE 4 4 4 4\n")
        output_file.write("TYPE F F F F\n")
        output_file.write("COUNT 1 1 1 1\n")
        output_file.write(f"WIDTH {len(lines)}\n")
        output_file.write("HEIGHT 1\n")
        output_file.write("VIEWPOINT 0 0 0 1 0 0 0\n")
        output_file.write(f"POINTS {len(lines)}\n")
        output_file.write("DATA ascii\n")

        output_file.writelines(lines)

    print("Finished processing the OSM file and saved the results to output.txt")

if __name__ == "__main__":
    main()
