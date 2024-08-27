board=[[2,7,4,9,2,3],[1,4,8,4,9,2],[7,5,9,0,6,7],[2,5,4,7,2,3],[6,7,8,0,4,3]]

def printboard():
    COLORS = {
        1:  '\033[34m',  # Blue
        2:  '\033[32m',  # Green
        3:  '\033[31m',  # Red
        4:  '\033[94m',  # Dark Blue
        5:  '\033[35m',  # Purple
        6:  '\033[36m',  # Turquoise
        7:  '\033[30m',  # Black
        8:  '\033[37m',  # Gray
        "M":'\033[31m'   # Red
    }
    RESET = '\033[0m'
    
    for row in board:
        formatted_row = []
        for item in row:
            color = COLORS.get(item, '')  # Default to no color if item is not in COLORS
            formatted_row.append(f"{color}{item}{RESET}")
        print(' '.join(formatted_row))
printboard()