import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
import ctypes
import sys

def clear():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def print_status(message, status="info"):
    timestamp = time.strftime("[%H:%M:%S]")
    if status == "error":
        print(f"{timestamp} \033[91m{message}\033[0m")  # Red
    elif status == "success":
        print(f"{timestamp} \033[92m{message}\033[0m")  # Green
    elif status == "warning":
        print(f"{timestamp} \033[93m{message}\033[0m")  # Yellow
    else:
        print(f"{timestamp} {message}")

def generate_tweet():
    """Generate a random motivational tweet."""
    tweets = [
        "Success is not final, failure is not fatal: it is the courage to continue that counts",
        "Believe you can and you're halfway there",
        "The future belongs to those who believe in their dreams",
        "Don't watch the clock; do what it does. Keep going",
        "The only way to do great work is to love what you do",
        "Your dreams don't work unless you do",
        "Push yourself, because no one else is going to do it for you",
        "The harder you work for something, the greater you'll feel when you achieve it",
        "Dream big and dare to fail",
        "Wake up with determination, go to bed with satisfaction",
        "Do something today that your future self will thank you for",
        "Little things make big days",
        "It's going to be hard, but hard does not mean impossible",
        "Don't stop when you're tired. Stop when you're done",
        "The only bad workout is the one that didn't happen",
        "Your limitation—it's only your imagination",
        "Sometimes later becomes never. Do it now",
        "Great things never come from comfort zones",
        "Success doesn't just find you. You have to go out and get it",
        "The key to success is to focus on goals, not obstacles",
        "Dream it. Believe it. Build it",
        "Your time is limited, don't waste it",
        "The best way to predict the future is to create it",
        "Small progress is still progress. Keep going",
        "Make it happen. Shock everyone",
        "You are stronger than you think",
        "Challenge yourself to be better every day",
        "Hard work beats talent when talent doesn't work hard",
        "Be the energy you want to attract",
        "Focus on your goals. The rest is just noise"
    ]
    return random.choice(tweets)

def post_tweet_with_shortcut(driver, consecutive_failures):
    try:
        # If we've had multiple failures, take a shorter break
        if consecutive_failures > 2:
            wait_time = min(60 * (consecutive_failures - 2), 300)  # Max 5 minutes
            print_status(f"Taking a {wait_time/60:.1f} minute break due to multiple failures...", "warning")
            time.sleep(wait_time)

        # Go to home page
        driver.get("https://twitter.com/home")
        time.sleep(2)  # Reduced wait time

        # Generate tweet text
        tweet_text = generate_tweet()
        tweet_text = f"{tweet_text} #MO3tasem"
        print_status(f"Attempting to post tweet: {tweet_text}", "info")

        # Use keyboard shortcut 'n' to open compose tweet
        webdriver.ActionChains(driver).send_keys('n').perform()
        time.sleep(1)  # Reduced wait time

        # Find tweet input using multiple selectors
        selectors = [
            "//div[@role='textbox' and @aria-label='Tweet text']",
            "//div[@data-testid='tweetTextarea_0']",
            "//div[@class='public-DraftEditor-content']",
            "//div[@contenteditable='true']"
        ]
        
        tweet_input = None
        for selector in selectors:
            try:
                tweet_input = WebDriverWait(driver, 3).until(  # Reduced wait time
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                if tweet_input:
                    break
            except:
                continue

        if not tweet_input:
            raise Exception("Could not find tweet input field")

        # Clear any existing text
        tweet_input.clear()
        time.sleep(0.5)  # Reduced wait time

        # Type tweet text faster
        for char in tweet_text:
            tweet_input.send_keys(char)
            time.sleep(random.uniform(0.02, 0.05))  # Faster typing

        time.sleep(0.5)  # Reduced wait time

        # Try to find tweet button with multiple selectors
        button_selectors = [
            "//div[@data-testid='tweetButtonInline']",
            "//div[@data-testid='tweetButton']",
            "//span[text()='Tweet']/..",
            "//div[@role='button'][contains(.,'Tweet')]"
        ]

        tweet_button = None
        for selector in button_selectors:
            try:
                tweet_button = WebDriverWait(driver, 3).until(  # Reduced wait time
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                if tweet_button:
                    break
            except:
                continue

        if not tweet_button:
            # Try keyboard shortcut as fallback
            webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()
        else:
            # Click the button if found
            driver.execute_script("arguments[0].click();", tweet_button)

        time.sleep(2)  # Reduced wait time

        # Go to profile to verify
        try:
            profile_link = WebDriverWait(driver, 5).until(  # Reduced wait time
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="AppTabBar_Profile_Link"]'))
            )
            profile_url = profile_link.get_attribute('href')
            driver.get(profile_url)
            time.sleep(2)  # Reduced wait time

            # Look for the tweet using multiple selectors
            tweet_found = False
            selectors = [
                'article[data-testid="tweet"]',
                'div[data-testid="tweet"]',
                'div[data-testid="tweetText"]'
            ]
            
            for selector in selectors:
                try:
                    tweets = WebDriverWait(driver, 3).until(  # Reduced wait time
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                    )
                    
                    # Check the most recent tweets
                    for tweet in tweets[:5]:
                        if tweet_text in tweet.text:
                            print_status("Tweet verified on profile!", "success")
                            return True
                except:
                    continue

            print_status("Tweet not found on profile", "error")
            return False

        except Exception as e:
            print_status(f"Error verifying tweet: {str(e)}", "error")
            return False

    except Exception as e:
        print_status(f"Error in post_tweet: {str(e)}", "error")
        return False

def find_and_interact_with_tweets(driver):
    try:
        # Navigate to home timeline
        driver.get("https://twitter.com/home")
        time.sleep(5)

        # Find tweets to interact with
        tweets = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
        )

        # Interact with up to 10 tweets
        for tweet in tweets[:10]:
            try:
                # Like the tweet
                like_button = tweet.find_element(By.CSS_SELECTOR, '[data-testid="like"]')
                driver.execute_script("arguments[0].click();", like_button)
                time.sleep(random.uniform(2, 4))

                # Retweet
                retweet_button = tweet.find_element(By.CSS_SELECTOR, '[data-testid="retweet"]')
                driver.execute_script("arguments[0].click();", retweet_button)
                time.sleep(random.uniform(1, 2))
                
                # Click the confirm retweet button
                confirm_retweet = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="retweetConfirm"]'))
                )
                driver.execute_script("arguments[0].click();", confirm_retweet)
                time.sleep(random.uniform(2, 4))

            except Exception as e:
                print_status(f"Error interacting with tweet: {str(e)}", "error")
                continue

    except Exception as e:
        print_status(f"Error finding tweets: {str(e)}", "error")

def twitter_bot(username, password):
    tweet_count = 0
    consecutive_failures = 0
    clear()
    
    # Print banner
    print("╔══════════════════════════════════════════╗")
    print("║            Twitter Bot v1.0              ║")
    print("║         Created by: Motasem              ║")
    print("║    https://github.com/mohasbks           ║")
    print("╚══════════════════════════════════════════╝")
    print("\n")

    try:
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # Re-enable headless mode
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--enable-javascript")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize driver
        print_status("Initializing browser in headless mode...", "info")
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'})
        
        # Set window size
        driver.set_window_size(1920, 1080)
        
        # Log in to Twitter
        print_status("Logging in to Twitter...")
        driver.get("https://twitter.com/login")
        time.sleep(5)
        
        # Enter username
        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
        )
        username_input.send_keys(username)
        username_input.send_keys(Keys.RETURN)
        time.sleep(3)
        
        # Enter password
        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
        )
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)
        
        print_status("Successfully logged in!", "success")
        
        while True:
            try:
                # First post 40 tweets
                print_status("Starting tweet posting session...", "info")
                tweets_posted = 0
                max_retries = 3

                while tweets_posted < 40:
                    for _ in range(max_retries):
                        if post_tweet_with_shortcut(driver, consecutive_failures):
                            tweet_count += 1
                            tweets_posted += 1
                            consecutive_failures = 0
                            print_status(f"Successfully posted and verified tweet #{tweet_count}", "success")
                            time.sleep(random.uniform(5, 10))  # Reduced delay between tweets
                            break
                        else:
                            consecutive_failures += 1
                            print_status("Tweet failed or not verified, retrying...", "warning")
                            time.sleep(random.uniform(10, 15))  # Reduced retry delay
                    else:  # If all retries failed
                        print_status("Max retries reached for this tweet, moving to next", "warning")
                        time.sleep(30)  # Reduced delay after max retries
                
                # After 40 tweets, interact with other tweets
                print_status("Starting tweet interactions...", "info")
                find_and_interact_with_tweets(driver)
                
                # Random wait time between batches (3-5 minutes)
                wait_time = random.uniform(180, 300)  # Reduced batch wait time
                print_status(f"Completed {tweets_posted} verified tweets and interactions. Waiting {wait_time/60:.1f} minutes before next session...", "info")
                time.sleep(wait_time)
                consecutive_failures = 0  # Reset failure counter after successful batch
            
            except Exception as e:
                print_status(f"Error in main loop: {str(e)}", "error")
                consecutive_failures += 1
                wait_time = min(120 * consecutive_failures, 900)  # Max 15 minutes
                print_status(f"Waiting {wait_time} seconds before retrying...", "warning")
                time.sleep(wait_time)
                continue
            
    except KeyboardInterrupt:
        print_status("\nBot stopped by user", "warning")
    except Exception as e:
        print_status(f"An error occurred: {str(e)}", "error")
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    clear()
    print("[*] Initializing Twitter Bot...")
    print(" [*] Press Ctrl+C to stop the bot")
    
    if len(sys.argv) != 3:
        print("Error: Please provide Twitter username and password")
        print("Usage: python twitter_bot.py <username> <password>")
        sys.exit(1)
        
    username = sys.argv[1]
    password = sys.argv[2]
    
    try:
        twitter_bot(username, password)
    except KeyboardInterrupt:
        print("\n[!] Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] An error occurred: {str(e)}")
        sys.exit(1)
