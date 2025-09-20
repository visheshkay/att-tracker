import os
import argparse
import pandas as pd
from face_check import main, init_face_app, detect_faces_in_image, get_embedding_for_image, match_student_to_class
# command to run python export_attendance.py --students_dir ./student-faces-1 --class_image ./test2.jpg --out_excel attendance.xlsx
def export_attendance(students_dir, class_image, out_excel, threshold=0.55, ctx=-1, min_face_size=60):
    # Run face_check pipeline
    import types
    args = types.SimpleNamespace(
        students_dir=students_dir,
        class_image=class_image,
        out=None,
        threshold=threshold,
        ctx=ctx,
        min_face_size=min_face_size,
    )
    results = main(args)

    # Build dataframe
    rows = []
    for r in results:
        roll = r["name"]
        status = "P" if r["found"] else "A"
        rows.append({"Roll No": roll, "Attendance": status})

    df = pd.DataFrame(rows)
    df.to_excel(out_excel, index=False)
    print(f"✅ Attendance exported to {out_excel}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--students_dir", required=True, help="Directory with student images")
    p.add_argument("--class_image", required=True, help="Class image")
    p.add_argument("--out_excel", default="attendance.xlsx", help="Output Excel file")
    p.add_argument("--threshold", type=float, default=0.45)
    p.add_argument("--ctx", type=int, default=-1)
    p.add_argument("--min_face_size", type=int, default=40)
    args = p.parse_args()

    export_attendance(args.students_dir, args.class_image, args.out_excel,
                      threshold=args.threshold, ctx=args.ctx, min_face_size=args.min_face_size)
