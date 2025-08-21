import csv
import os
import sys

# ==================== USER SETTINGS =======================
OUTPUT_HEADER = True     # Add header to CSV
MIRROR_Z = True          # Mirrors Z (for Blender import compatibility)
# ==========================================================

def parse_obj(obj_path):
    verts = []
    uvs = []
    faces = []

    with open(obj_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()
                x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                if MIRROR_Z:
                    z = -z
                verts.append((x, y, z))
            elif line.startswith('vt '):
                parts = line.strip().split()
                u, v = float(parts[1]), float(parts[2])
                uvs.append((u, v))
            elif line.startswith('f '):
                parts = line.strip().split()[1:]
                face = []
                for part in parts:
                    idx = part.split('/')[0]  # format: v/vt
                    face.append(int(idx))
                faces.append(tuple(face))

    return verts, uvs, faces

def write_csv(csv_path, verts, uvs, faces):
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)

        if OUTPUT_HEADER:
            writer.writerow(["Index", "FaceIndex", "X", "Y", "Z", "U", "V"])

        idx = 0
        for face_id, face in enumerate(faces, start=1):
            for vert_idx in face:
                v = verts[vert_idx - 1]
                uv = uvs[vert_idx - 1] if vert_idx - 1 < len(uvs) else (0.0, 0.0)
                writer.writerow([idx, face_id, v[0], v[1], v[2], uv[0], uv[1]])
                idx += 1

def convert_obj_to_csv(obj_path):
    verts, uvs, faces = parse_obj(obj_path)
    csv_path = os.path.splitext(obj_path)[0] + ".csv"
    write_csv(csv_path, verts, uvs, faces)
    print(f"Saved: {csv_path}")

def main():
    if len(sys.argv) < 2:
        print("Drag and drop one or more OBJ files onto this script.")
        return

    for arg in sys.argv[1:]:
        if arg.lower().endswith(".obj") and os.path.isfile(arg):
            try:
                print(f"Processing: {arg}")
                convert_obj_to_csv(arg)
            except Exception as e:
                print(f"Error processing {arg}: {e}")
        else:
            print(f"Skipped: {arg} (not a .obj file)")

if __name__ == "__main__":
    main()
