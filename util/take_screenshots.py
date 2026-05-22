import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Launch browser (headless by default)
        browser = await p.chromium.launch()
        # Create context with portrait mobile/kiosk viewport
        context = await browser.new_context(
            viewport={"width": 1080, "height": 1920},
            user_agent="Mozilla/5.0 (Linux; Android 10; Kiosk) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Mobile Safari/537.36"
        )
        page = await context.new_page()
        
        # Navigate to local server
        print("Navigating to http://localhost:8000/index.html ...")
        await page.goto("http://localhost:8000/index.html")
        
        # 1. Wait for loader to disappear
        print("Waiting for loader to disappear...")
        await page.wait_for_selector("#loader", state="hidden")
        await asyncio.sleep(0.5)
        
        # Capture Splash Screen
        artifact_dir = r"C:\Users\Buvi\.gemini\antigravity\brain\71ecd954-8dd0-490b-a69c-61affdd031d9"
        splash_path = os.path.join(artifact_dir, "test_splash.png")
        await page.screenshot(path=splash_path)
        print(f"Captured Splash screen: {splash_path}")
        
        # 2. Click on Splash to start
        print("Clicking Splash screen to proceed to birthday selection...")
        await page.click("#phase-splash")
        await asyncio.sleep(1.0) # wait for transition
        
        # Capture Birthday Selector
        birth_path = os.path.join(artifact_dir, "test_birthday.png")
        await page.screenshot(path=birth_path)
        print(f"Captured Birthday screen: {birth_path}")
        
        # 3. Confirm Birthday
        print("Confirming birthday...")
        await page.click("button:has-text('이 날짜로 점치기')")
        
        # Wait for the intro narrative to complete and cards to appear
        print("Waiting for Zodiac cards to load...")
        await page.wait_for_selector("#cards-area .card-container", timeout=8000)
        await asyncio.sleep(1.2) # Allow stagger entrance animation to complete
        
        # Capture Phase 1: Zodiac
        zodiac_path = os.path.join(artifact_dir, "test_pick_zodiac.png")
        await page.screenshot(path=zodiac_path)
        print(f"Captured Zodiac Pick screen: {zodiac_path}")
        
        # 4. Click a card in Zodiac
        print("Clicking first Zodiac card...")
        # Get first card
        cards = await page.query_selector_all("#cards-area .card-container")
        if cards:
            await cards[0].click()
            print("Clicked Zodiac card. Waiting for narrative...")
            await page.wait_for_selector("#narrative-overlay.active", timeout=4000)
            await asyncio.sleep(1.2) # Wait for flip and fade in
            
            # Capture Zodiac Card Narrative
            zodiac_narr_path = os.path.join(artifact_dir, "test_zodiac_narrative.png")
            await page.screenshot(path=zodiac_narr_path)
            print(f"Captured Zodiac Narrative: {zodiac_narr_path}")
            
            # Click narrative overlay to skip
            print("Clicking narrative overlay to skip...")
            await page.click("#narrative-overlay")
            await page.wait_for_selector("#narrative-overlay:not(.active)", timeout=4000)
            await asyncio.sleep(2.0) # Wait for next step stagger entry animation
        else:
            print("No cards found in Zodiac phase!")
            
        # Capture Phase 2: Planet
        planet_path = os.path.join(artifact_dir, "test_pick_planet.png")
        await page.screenshot(path=planet_path)
        print(f"Captured Planet Pick screen: {planet_path}")
        
        # 5. Click a card in Planet
        print("Clicking Planet card...")
        cards = await page.query_selector_all("#cards-area .card-container")
        if cards:
            await cards[0].click()
            print("Clicked Planet card. Waiting for narrative...")
            await page.wait_for_selector("#narrative-overlay.active", timeout=4000)
            await asyncio.sleep(1.2)
            
            # Capture Planet Card Narrative
            planet_narr_path = os.path.join(artifact_dir, "test_planet_narrative.png")
            await page.screenshot(path=planet_narr_path)
            
            # Click overlay to skip
            print("Clicking narrative overlay to skip...")
            await page.click("#narrative-overlay")
            await page.wait_for_selector("#narrative-overlay:not(.active)", timeout=4000)
            await asyncio.sleep(2.0)
            
        # Capture Phase 3: Element
        element_path = os.path.join(artifact_dir, "test_pick_element.png")
        await page.screenshot(path=element_path)
        print(f"Captured Element Pick screen: {element_path}")
        
        # 6. Click a card in Element
        print("Clicking Element card...")
        cards = await page.query_selector_all("#cards-area .card-container")
        if cards:
            await cards[0].click()
            print("Clicked Element card. Waiting for narrative...")
            await page.wait_for_selector("#narrative-overlay.active", timeout=4000)
            await asyncio.sleep(1.2)
            
            # Capture Element Card Narrative
            element_narr_path = os.path.join(artifact_dir, "test_element_narrative.png")
            await page.screenshot(path=element_narr_path)
            
            # Click overlay to skip
            print("Clicking narrative overlay to skip...")
            await page.click("#narrative-overlay")
            await page.wait_for_selector("#narrative-overlay:not(.active)", timeout=4000)
            
        # Capture Final Result (Phase 4)
        print("Waiting for Final Result phase...")
        await page.wait_for_selector("#phase-4.active", timeout=8000)
        await asyncio.sleep(1.5) # Wait for ticket slide/fade animations
        result_path = os.path.join(artifact_dir, "test_result.png")
        await page.screenshot(path=result_path)
        print(f"Captured Result screen: {result_path}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
