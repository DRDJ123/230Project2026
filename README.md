# 230Project2026
# Raspberry Pi Arcade Project – 230 Project 2026

## 1. Project Overview

This project is a Raspberry Pi arcade system with three playable games:

- Tetris
- Bird Run
- Flappy Bird

Players enter their name in the launcher, select a game, and play. Each game submits the player's score to a shared leaderboard.

The project uses two Raspberry Pis:

| Raspberry Pi | Purpose |
|---|---|
| Pi #1 | Runs the launcher and all three games |
| Pi #2 | Runs the leaderboard server and stores scores |

Both Raspberry Pis must be connected to the same wired local network for score submissions and the leaderboard webpage to work.

---

## 2. What You Need

Before starting, gather:

- Two Raspberry Pis
- Two power supplies
- Two Ethernet cables
- A router or network switch with available Ethernet ports
- A monitor, keyboard, and mouse for initial setup
- A computer with internet access
- A working Raspberry Pi OS installation on both Pis

You will also need both Raspberry Pis connected to the same local network.

---

## 3. Connect the Raspberry Pis to the Wired Network

1. Connect an Ethernet cable from **Pi #1** to an available LAN port on the router or network switch.
2. Connect another Ethernet cable from **Pi #2** to another LAN port on the same router or switch.
3. If you are using a network switch, make sure the switch is also connected to the router.
4. Power on both Raspberry Pis.
5. Make sure both Pis have network connections.

**Important:** Do not connect the two Raspberry Pis directly to each other with only one Ethernet cable. Connect both to the same router or network switch.

### Configure Pi #2's network address

The game computers send scores to the local address

Pi #2 must use this address so Pi #1 can find the leaderboard server.

The recommended method is to create a DHCP reservation in the router:

1. Open the router's administration page on a computer connected to the network.
2. Find the DHCP reservation or address reservation settings.
3. Find Pi #2 in the connected-device list.
4. Reserve the local address for Pi #2.
5. Save the router settings.
6. Restart Pi #2's network connection or reboot Pi #2.

Make sure the router's network uses your address range and that the local address is available. Do not assign this address to another device.

On Pi #2, open a terminal and check its address:

```bash
hostname -I
```

The output should include:

```text
'your local address'
```

Pi #1 can use automatic DHCP addressing. It must be connected to the same network.

---

## 4. Download the Project on Both Raspberry Pis

On **each Raspberry Pi**, open a terminal and install Git:

```bash
sudo apt update
sudo apt install -y git
```

Download the project:

```bash
git clone https://github.com/DRDJ123/230Project2026.git
```

This creates a folder named `230Project2026`.

---

## 5. Set Up Pi #2 – Leaderboard Server

IN "leaderboard" CODE EDIT LINE 11 

Pi #2 receives scores from the games and stores them in a SQLite database.

### Install Flask

On Pi #2, run:

```bash
sudo apt update
sudo apt install -y python3-flask
```

### Start the leaderboard server

Open a terminal on Pi #2:

```bash
cd ~/230Project2026/pi2-leaderboard
```

Start the server:

```bash
python3 app.py
```

The server should now be running on port `5000`.

Keep this terminal open while the arcade is being used. Closing the terminal stops the server.

### Open the leaderboard webpage

On a computer connected to the same network, open a web browser and visit:

pi 2s leaderboard webpage address

The page displays the top 10 scores for each game.

The server stores scores in `scores.db`. This database is created automatically when the server starts for the first time. Scores remain stored when the server is restarted.

---

## 6. Set Up Pi #1 – Games and Launcher

Pi #1 runs the game launcher and all three games.

### Install Pygame

On Pi #1, open a terminal and run:

```bash
sudo apt update
sudo apt install -y python3-pygame
```

### Prepare the game filenames

The launcher expects the game files to have `.py` extensions. After downloading the repository, rename the three game files:

```bash
cd ~/230Project2026

mv tetris tetris.py
mv birdrun bird_run.py
mv Flappy_bird flappy_bird.py
```

Do this only once on Pi #1.

### Start the arcade

Make sure the leaderboard server on Pi #2 is running.

On Pi #1, open a terminal and run:

```bash
cd ~/230Project2026
python3 launcher
```

The arcade launcher should appear.

1. Type your player name.
2. Use the **Up and Down arrow keys** to choose a game.
3. Press **Enter** to start playing.
4. Press **Esc** to exit the launcher.

---

## 7. How the Leaderboard Works

When a player finishes a game, the game sends the player's name, game name, and score to Pi #2.

The server receives the score through:

`http://(insert loacl ip):5000/score`

The server saves the score in its SQLite database.

The leaderboard webpage is available at:

`http://(insert loacl ip):5000`

It displays the top 10 scores for:

- Tetris
- Bird Run
- Flappy Bird

### Offline behavior

If Pi #2 is disconnected or the leaderboard server is not running, the games can still be played.

The game displays a message indicating that the score could not be uploaded. The score is not added to the shared leaderboard unless it is successfully submitted.

---

## 8. Testing the Network Connection

If scores are not appearing on the leaderboard, follow these steps.

### Test Pi #2

On Pi #2, check its IP address:

```bash
hostname -I
```

Confirm that it includes `(your address)`.

Make sure the server is running:

```bash
cd ~/230Project2026/pi2-leaderboard
python3 app.py
```

### Test Pi #1

On Pi #1, check that Pi #2 can be reached:

```bash
ping -c 4 (your address)
```

If the connection works, Pi #1 should receive replies.

If it does not work:

- Check that both Ethernet cables are connected.
- Check that both Pis are connected to the same router or switch.
- Confirm Pi #2 has the correct IP address.
- Make sure the leaderboard server is running.

### Test the leaderboard webpage

On a computer connected to the same network, visit:

`http://(insert loacl ip):5000/score`

If the webpage loads, the leaderboard server is reachable.

---

## 9. Project Files

| File or folder | Purpose |
|---|---|
| `launcher` | Starts the arcade menu and launches games |
| `leaderboard` | Shared code used to submit scores |
| `tetris.py` | Tetris game (renamed during Pi #1 setup) |
| `bird_run.py` | Bird Run game (renamed during Pi #1 setup) |
| `flappy_bird.py` | Flappy Bird game (renamed during Pi #1 setup) |
| `pi2-leaderboard/` | Leaderboard server and webpage |
| `scores.db` | Database created by the server to store scores |

---

## 10. Starting the Arcade After a Restart

After either Raspberry Pi has been restarted:

**On Pi #2:**

```bash
cd ~/230Project2026/pi2-leaderboard
python3 app.py
```

**On Pi #1:**

```bash
cd ~/230Project2026
python3 launcher
```

Keep the Pi #2 server running while playing games on Pi #1.

---

## 11. Troubleshooting

| Problem | Solution |
|---|---|
| Launcher cannot find a game | Make sure the three game files were renamed as described in Section 6. |
| Pygame is missing | Run `sudo apt install python3-pygame` on Pi #1. |
| Flask is missing | Run `sudo apt install python3-flask` on Pi #2. |
| Leaderboard webpage will not load | Make sure Pi #2 is running `app.py` and has the correct IP address. |
| Scores are not uploading | Check the Ethernet connections and make sure the server is running. |
| Scores disappear after restarting | Make sure Pi #2 is using the same `scores.db` file in the `pi2-leaderboard` folder. |

---

## 12. Repository

Project source code:

https://github.com/DRDJ123/230Project2026

**Project:** 230 Project 2026  
**System:** Raspberry Pi Arcade with Networked Leaderboard
