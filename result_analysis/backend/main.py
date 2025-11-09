from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import numpy as np

app = FastAPI()

origins = [
    "https://demo-analysis4sumi.onrender.com",  
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store uploaded DataFrame globally (for simplicity)
df_store = None

@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    global df_store
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    df = df.replace([np.inf, -np.inf], None)
    df = df.where(pd.notnull(df), None)
    df_store = df

    # --- Summary Computation ---
    if "Overall_Grade" in df.columns:
        total_students = len(df)
        passed_students = df[df["Overall_Grade"].astype(str) != "F"].shape[0]
        pass_percentage = round((passed_students / total_students) * 100, 2) if total_students > 0 else 0
    else:
        total_students = passed_students = pass_percentage = None

    return {
        "message": "File uploaded successfully",
        "columns": df.columns.tolist(),
        "summary": {
            "total_students": total_students,
            "passed_students": passed_students,
            "pass_percentage": pass_percentage
        }
    }



# @app.get("/unique/{column}")
# async def get_unique_values(column: str):
#     global df_store
#     if df_store is None:
#         raise HTTPException(status_code=400, detail="No CSV uploaded yet.")
#     if column not in df_store.columns:
#         raise HTTPException(status_code=400, detail="Invalid column name.")
#     unique_vals = df_store[column].dropna().unique().tolist()
#     return {"unique_values": unique_vals}

@app.get("/unique/{column}")
async def get_unique_values(column: str):
    global df_store
    if df_store is None:
        raise HTTPException(status_code=400, detail="No CSV uploaded yet.")

    # Only allow columns that end with 'Grade'
    # valid_columns = [col for col in df_store.columns if col.endswith("Grade")]


    if column not in df_store:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid column name. Only columns ending with 'Grade' are allowed. Valid options: {df_store}"
        )

    unique_vals = df_store[column].dropna().unique().tolist()
    return {"unique_values": unique_vals}



@app.get("/count/{column}/{value}")
async def get_value_count(column: str, value: str):
    global df_store
    if df_store is None:
        raise HTTPException(status_code=400, detail="No CSV uploaded yet.")
    if column not in df_store.columns:
        raise HTTPException(status_code=400, detail="Invalid column name.")
    count = df_store[df_store[column].astype(str) == value].shape[0]
    return {"count": int(count)}

@app.get("/grades")
async def get_grade_columns():
    global df_store
    if df_store is None:
        return {"grade_columns": []}

    grade_cols = [col for col in df_store.columns if col.lower().endswith("grade")]
    return {"grade_columns": grade_cols}

@app.get("/gradesummary/{column}")
async def get_grade_summary(column: str):
    global df_store
    if df_store is None:
        raise HTTPException(status_code=400, detail="No CSV uploaded yet.")
    if column not in df_store.columns:
        raise HTTPException(status_code=400, detail="Invalid column name.")

    total_students = len(df_store)
    passed_students = df_store[df_store[column].astype(str) != "F"].shape[0]
    pass_percentage = round((passed_students / total_students) * 100, 2) if total_students > 0 else 0

    return {
        "column": column,
        "total_students": total_students,
        "passed_students": passed_students,
        "pass_percentage": pass_percentage
    }


@app.get("/gradesummary_full")
async def get_full_grade_summary():
    global df_store
    if df_store is None:
        raise HTTPException(status_code=400, detail="No CSV uploaded yet.")
    
    results = []
    total_students = len(df_store)

    # Identify all columns ending with 'Grade'
    grade_cols = [col for col in df_store.columns if col.lower().endswith("grade")]

    for grade_col in grade_cols:
        subject = grade_col.replace("_Grade", "").replace("grade", "").strip("_ ")
        marks_col = None
        for c in df_store.columns:
            if c.lower() == f"{subject.lower()}_marks":
                marks_col = c
                break

        # Compute pass stats
        passed_students = df_store[df_store[grade_col].astype(str) != "F"].shape[0]
        pass_percentage = round((passed_students / total_students) * 100, 2) if total_students > 0 else 0

        # Find topper if marks column exists
        topper = None
        if marks_col and marks_col in df_store.columns:
            try:
                top_idx = df_store[marks_col].astype(float).idxmax()
                topper_row = df_store.loc[top_idx]
                topper = {
                    "name": str(topper_row.get("Name", "N/A")),
                    "register_number": str(topper_row.get("Register_Number", "N/A")),
                    "marks": float(topper_row.get(marks_col, 0)),
                    "grade": str(topper_row.get(grade_col, "N/A"))
                }
            except Exception:
                topper = None

        results.append({
            "subject": subject,
            "grade_column": grade_col,
            "marks_column": marks_col,
            "passed_students": int(passed_students),
            "pass_percentage": pass_percentage,
            "topper": topper
        })

    return {"summary": results}


@app.get("/overall_summary")
async def get_overall_summary():
    global df_store
    if df_store is None:
        raise HTTPException(status_code=400, detail="No CSV uploaded yet.")
    
    if "Overall_Grade" not in df_store.columns:
        raise HTTPException(status_code=400, detail="'Overall_Grade' column not found in uploaded CSV.")
    
    # Count each grade
    grade_counts = df_store["Overall_Grade"].astype(str).value_counts().sort_index()

    # Build dictionary {grade: count}
    grade_dict = grade_counts.to_dict()

    # Prepare response in your desired structure
    return {
        "grades": list(grade_dict.keys()),
        "counts": list(grade_dict.values())
    }


# @app.get("/class_topper")
# async def get_class_topper():
#     global df_store
#     if df_store is None:
#         raise HTTPException(status_code=400, detail="No CSV uploaded yet.")
    
#     if "Total" not in df_store.columns:
#         raise HTTPException(status_code=400, detail="'Total' column not found in uploaded CSV.")
    
#     # Identify topper row
#     topper_row = df_store.loc[df_store["Total"].idxmax()]

#     # Try to auto-detect common columns
#     name_col = next((c for c in df_store.columns if "name" in c.lower()), None)
#     reg_col = next((c for c in df_store.columns if "reg" in c.lower()), None)
#     grade_col = next((c for c in df_store.columns if "overall_grade" in c.lower()), None)

#     topper_details = {
#         "name": topper_row[name_col] if name_col else None,
#         "register_number": topper_row[reg_col] if reg_col else None,
#         "total_marks": int(np.int64(topper_row["Total"])), 
#         "overall_grade": topper_row[grade_col] if grade_col else None
#     }

#     print(topper_details)
    

#     return topper_details

@app.get("/class_topper")
async def get_class_topper():
    global df_store
    if df_store is None:
        raise HTTPException(status_code=400, detail="No CSV uploaded yet.")
    
    if "Total" not in df_store.columns:
        raise HTTPException(status_code=400, detail="'Total' column not found in uploaded CSV.")

    # ✅ Convert 'Total' to numeric safely
    df_store["Total"] = pd.to_numeric(df_store["Total"], errors="coerce")

    # ✅ Drop rows without numeric totals
    valid_df = df_store.dropna(subset=["Total"])
    if valid_df.empty:
        raise HTTPException(status_code=400, detail="No valid numeric 'Total' values found.")

    # ✅ Identify topper row safely
    topper_row = valid_df.loc[valid_df["Total"].idxmax()]

    # Auto-detect common columns
    name_col = next((c for c in df_store.columns if "name" in c.lower()), None)
    reg_col = next((c for c in df_store.columns if "reg" in c.lower()), None)
    grade_col = next((c for c in df_store.columns if "overall_grade" in c.lower()), None)

    topper_details = {
        "name": topper_row[name_col] if name_col else None,
        "register_number": topper_row[reg_col] if reg_col else None,
        "total_marks": int(topper_row["Total"]),
        "overall_grade": topper_row[grade_col] if grade_col else None
    }

    print(topper_details)
    return topper_details










