import re
import json

def parse_ab_output(file_path):
    data = {
        "connection_times": {},
        "percentage_of_requests_served_within_time": {},
        "test_metadata": {}
    }

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if "Requests per second" in line:
            data["requests_per_second"] = float(re.search(r":\s*([\d\.]+)", line).group(1))
        elif "Time per request" in line and "[ms] (mean)" in line:
            data["time_per_request_mean"] = float(re.search(r":\s*([\d\.]+)", line).group(1))
        elif "Transfer rate" in line:
            data["transfer_rate"] = float(re.search(r":\s*([\d\.]+)", line).group(1))
        elif re.match(r"\s+min\s+mean\[", line):
            # Assuming the next four lines contain the data for connect, processing, waiting, total
            for _ in range(4):
                next_line = next(lines)
                if "Connect:" in next_line:
                    data["connection_times"]["connect"] = [float(x) for x in re.findall(r"\d+", next_line)]
                elif "Processing:" in next_line:
                    data["connection_times"]["processing"] = [float(x) for x in re.findall(r"\d+", next_line)]
                elif "Waiting:" in next_line:
                    data["connection_times"]["waiting"] = [float(x) for x in re.findall(r"\d+", next_line)]
                elif "Total:" in next_line:
                    data["connection_times"]["total"] = [float(x) for x in re.findall(r"\d+", next_line)]
        elif re.match(r"\s+\d+%.*", line):
            # Match lines like "  50%      2"
            match = re.search(r"(\d+)%\s+(\d+)", line)
            if match:
                percentile = match.group(1) + "_percent"
                time = int(match.group(2))
                data["percentage_of_requests_served_within_time"][percentile] = time
        elif "Server Software:" in line:
            data["test_metadata"]["server_software"] = line.split(":")[1].strip()
        # Add more parsing rules as needed

    return data

def save_as_json(data, output_file):
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
file_path = 'result.txt'  # ApacheBench output file
output_json_file = 'ab_output.json'


ab_data = parse_ab_output(file_path)

# JSON 파일로 저장
save_as_json(ab_data, output_json_file)

