import subprocess
import shutil
import os

def run_step(cmd, cwd=None):
    print(f"\n>>> Running: {cmd}")
    subprocess.run(cmd, cwd=cwd, check=True)

def main():
    # Step 1: Generate dataset
    run_step(["py", "generate_dataset.py"], cwd="../data")

    # Step 2: Run SQL queries
    run_step(["py", "run_queries.py"], cwd="../Part1_SQL")

    # Step 3: Run Growth Engine tests
    run_step(["py", "-m", "pytest", "-v"], cwd="../Part2_Engine")

    # Step 4: Copy narrative report into output
    src = "../Part3_Narrative/narrative_report.md"
    dest_dir = "output"
    os.makedirs(dest_dir, exist_ok=True)
    dest_file = os.path.join(dest_dir, "narrative_report.md")
    shutil.copy(src, dest_file)
    print(f"\nNarrative report copied to {dest_file}")

    # Step 5: Print narrative report content
    print("\n===== Narrative Report =====\n")
    with open(dest_file, "r", encoding="utf-8") as f:
        print(f.read())
    print("\n===== End of Narrative =====")

if __name__ == "__main__":
    main()
