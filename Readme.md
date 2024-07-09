### Prerequisites
- Python and pip installed

### Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/khanmdnasir/nybsys_ftp_automation.git
   cd nybsys_ftp_automation
   ```

2. **Create a virtual environment named like env with Python's venv:**

    ```sh
    python3 -m venv venv
    ```

  - Activate the virtual environment (For Ubuntu/Mac):
    ```bash
    source venv/bin/activate
    ```
  - For Windows:
    ```bash
    venv\Scripts\activate
    ```

3. **Installation**
- Install all requirements for project

    ```bash
    pip install -r requirements.txt
    ```
  
4**Environment Variable**
    
- Create a `.env` file in the root directory of the project. Get necessary variable names from `.env.example` and use appropriate values according to environment.

- Or run a command on terminal, 
    ```bash
    cp .env.example .env
    ```


### Run script
Run this script locally
```bash
python main.py
```
