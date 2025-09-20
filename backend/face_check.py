#!/usr/bin/env python3
"""
face_check.py

Usage:
  python face_check.py --students_dir ./student-faces-1 --class_image ./test2.jpg --out output.png --excel attendance.xlsx --threshold 0.45 --ctx -1

Requirements:
  pip install insightface onnxruntime opencv-python-headless numpy pandas openpyxl
"""

import os
import argparse
import cv2
import numpy as np
import pandas as pd
from math import isfinite
from datetime import date  

try:
    from insightface.app import FaceAnalysis
except Exception as e:
    raise RuntimeError(
        "Failed to import insightface. Make sure insightface and onnxruntime are installed and compatible with your NumPy version.\n"
        "If you want a lighter CPU-only route, consider using 'face_recognition' instead."
    ) from e


def init_face_app(ctx_id=-1, det_size=(640, 640)):
    app = FaceAnalysis(name="antelopev2", allowed_modules=['detection', 'recognition'])
    app.prepare(ctx_id=ctx_id, det_size=det_size)
    return app


def read_image(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Unable to read image: {path}")
    return img


def largest_face(faces):
    if not faces:
        return None
    areas = [(f, (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1])) for f in faces]
    return max(areas, key=lambda x: x[1])[0]


def get_embedding_for_image(app, img_path):
    img = read_image(img_path)
    faces = app.get(img)
    if not faces:
        return None
    face = largest_face(faces)
    if face is None:
        return None
    emb = np.array(face.embedding, dtype=np.float32)
    norm = np.linalg.norm(emb)
    if norm > 0:
        emb = emb / norm
    return emb


def detect_faces_in_image(app, img_path, min_face_size=40):
    img = read_image(img_path)
    faces = app.get(img)
    out = []
    for f in faces:
        x1, y1, x2, y2 = [int(round(v)) for v in f.bbox[:4]]
        if (x2-x1) < min_face_size or (y2-y1) < min_face_size:
            continue
        emb = np.array(f.embedding, dtype=np.float32)
        n = np.linalg.norm(emb)
        if n > 0:
            emb = emb / n
        out.append({
            "bbox": [x1, y1, x2, y2],
            "embedding": emb,
            "score": float(getattr(f, 'det_score', 0.0))
        })
    return out


def cosine_similarity_vec(a, b):
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0 or not isfinite(denom):
        return -1.0
    return float(np.dot(a, b) / denom)


def match_student_to_class(student_emb, class_faces, threshold=0.55):
    best_score, best_idx = -1.0, None
    for i, f in enumerate(class_faces):
        score = cosine_similarity_vec(student_emb, f["embedding"])
        if score > best_score:
            best_score, best_idx = score, i
    if best_score >= threshold:
        return True, best_score, best_idx
    return False, best_score, best_idx


def draw_matches(class_image_path, results, out_path):
    img = read_image(class_image_path)
    for r in results:
        if not r.get("found"):
            continue
        x1, y1, x2, y2 = r["bbox"]
        label = f"{r['name']} {r['score']:.2f}"
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 200, 0), 2)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 6, y1), (0, 200, 0), -1)
        cv2.putText(img, label, (x1 + 3, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.imwrite(out_path, img)


def export_to_excel(results, out_excel):
    today = date.today().strftime("%Y-%m-%d")  # format as YYYY-MM-DD
    rows = []
    for r in results:
        roll = r["name"]
        status = "P" if r["found"] else "A"
        rows.append({
            "Roll No": roll,
            "Attendance": status,
            "Date": today
        })

    df = pd.DataFrame(rows)
    df.to_excel(out_excel, index=False)
    print(f"Excel file saved to {out_excel}")


def main(args):
    app = init_face_app(ctx_id=args.ctx, det_size=(640, 640))
    print("Detecting faces in class image...")
    class_faces = detect_faces_in_image(app, args.class_image, min_face_size=args.min_face_size)
    print(f"Detected {len(class_faces)} usable faces in class image.")

    # Explicitly allow .jpeg files
    exts = ('.jpg', '.jpeg')
    student_files = [os.path.join(args.students_dir, f)
                     for f in sorted(os.listdir(args.students_dir))
                     if f.lower().endswith(exts)]

    if not student_files:
        raise RuntimeError("No .jpg or .jpeg files found in students_dir")

    results = []
    for sfile in student_files:
        name = os.path.splitext(os.path.basename(sfile))[0]
        print(f"\nProcessing student image: {sfile} (name={name})")
        emb = get_embedding_for_image(app, sfile)
        if emb is None:
            print("  -> No face detected.")
            results.append({"name": name, "found": False, "score": None, "bbox": None})
            continue

        found, best_score, best_idx = match_student_to_class(emb, class_faces, threshold=args.threshold)
        if found:
            bbox = class_faces[best_idx]["bbox"]
            print(f"  -> FOUND. score={best_score:.4f}, bbox={bbox}")
            results.append({"name": name, "found": True, "score": best_score, "bbox": bbox})
        else:
            print(f"  -> NOT FOUND. best_score={best_score:.4f}")
            results.append({"name": name, "found": False, "score": best_score, "bbox": None})

    #  Save annotated class image
    if args.out:
        draw_matches(args.class_image, results, args.out)
        print(f"\nAnnotated image saved to: {args.out}")

    #  Save Excel attendance
    if args.excel:
        export_to_excel(results, args.excel)

    present = [r for r in results if r["found"]]
    absent = [r for r in results if not r["found"]]
    print("\nSummary:")
    print(f" Present ({len(present)}): {[r['name'] for r in present]}")
    print(f" Absent  ({len(absent)}): {[r['name'] for r in absent]}")

    return results


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--students_dir", required=True, help="Directory containing student images (1.jpeg,2.jpeg,...)")
    p.add_argument("--class_image", required=True, help="Path to class/group image (JPEG)")
    p.add_argument("--out", default="output.png", help="Annotated output image path")
    p.add_argument("--excel", default="attendance.xlsx", help="Excel file for attendance")
    p.add_argument("--threshold", type=float, default=0.55, help="Cosine similarity threshold")
    p.add_argument("--ctx", type=int, default=-1, help="ctx_id (-1 CPU, 0 GPU)")
    p.add_argument("--min_face_size", type=int, default=60, help="Minimum face height in px")
    args = p.parse_args()
    main(args)
