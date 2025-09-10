import os

def analyze_bus_log(bus_no):
    # 🔹 Build log file path based on bus number
    log_path = fr"C:\Users\User\Downloads\{bus_no}.log"

    if not os.path.exists(log_path):
        print(f"❌ Log file not found for bus {bus_no}: {log_path}")
        return

    audio_announcement = False
    all_stops = []   # store ALL stops from log file

    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line_clean = line.strip()
                line_lower = line_clean.lower()

                # ✅ Detect pending stops
                if "pending stops" in line_lower:
                    idx = line_lower.find("pending stops")
                    stop_part = line_clean[idx + len("pending stops"):].strip()

                    # Split by ; or , (support both)
                    stops = [s.strip() for s in stop_part.replace(",", ";").split(";") if s.strip()]
                    if stops:
                        all_stops.extend(stops)   # keep adding stops

                # ✅ Detect audio announcement
                if "audio announcement" in line_lower or "announcement" in line_lower:
                    audio_announcement = True

        # ✅ Remove duplicates but keep order
        seen = set()
        unique_stops = []
        for stop in all_stops:
            if stop not in seen:
                unique_stops.append(stop)
                seen.add(stop)

        # ✅ Print result
        print(f"\n📌 Bus No: {bus_no}")
        if audio_announcement:
            print("🔊 Audio Announcement: YES")

            if unique_stops:
                # Print all stops once
                print("🚌 All Pending Stops:")
                for stop in unique_stops:
                    print("   -", stop)

                # Show current & next stops in a loop
                print("\n➡ Journey Progression:")
                for i in range(len(unique_stops)):
                    current_stop = unique_stops[i]
                    if i + 1 < len(unique_stops):
                        next_stop = unique_stops[i + 1]
                        print(f"   🛑 Current Stop: {current_stop} → Next Stop: {next_stop}")
                    else:
                        print(f"   🏁 Final Stop Reached: {current_stop}")
            else:
                print("🚌 No pending stops found")
        else:
            print("🔊 Audio Announcement: NO")

    except Exception as e:
        print("⚠ Error reading file:", e)


# -------- Run the program --------
if __name__ == "__main__":
    bus_no = input("Enter Bus Number: ").strip()
    analyze_bus_log(bus_no)
