### How to run:

1. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     ./venv/Scripts/activate
     ```
   - On Linux:
     ```bash
     . ./venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
    ```bash
    python ./tpb_rss.py --host 127.0.0.1 --port 56789
    ```

### Accessing the RSS feed
You can access the RSS feed for your Pirate Bay search by modifying the search URL. Replace:
```
https://thepiratebay.org/search.php?q=<search query>
```
with:
```
http://localhost:56789/rss?q=<search query>
```

### Run it as a service on Linux:
1. Create and activate a virtual environment, then install dependencies:
   ```bash
   python3 -m venv venv
   . ./venv/bin/activate
   pip install -r requirements.txt
   pip install waitress
   ```

2. Create a new file in `/etc/systemd/system` called `tpb_rss.service` with the following contents:
   ```
   [Unit]
   Description=tpb rss server
   After=network.target

   [Service]
   ExecStart=<path/to/tpb_rss>/venv/bin/waitress-serve --host 127.0.0.1 --port 56789 tpb_rss:app
   WorkingDirectory=<path/to/tpb_rss>
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
   Replace `<path/to/tpb_rss>` with the full path to the project directory.

3. Reload the systemd daemon and enable the service:
   ```bash
   systemctl -q daemon-reload
   systemctl enable --now -q tpb_rss
   ```

Once the service is running, you can access the RSS feed by replacing:
```
https://thepiratebay.org/search.php?q=<search query>
```
with:
```
http://127.0.0.1:56789/rss?q=<search query>
```

#### Notes:
- To allow connections from other machines, change the `--host` parameter `0.0.0.0`.
- You can also change the port by modifying the `--port` parameter.