--based off crime scene reports check atm transactions for a withdrawl at the fifer location
SELECT name FROM people
WHERE id IN 
(SELECT person_id FROM bank_accounts
WHERE account_number IN 
(SELECT account_number FROM atm_transactions
WHERE day = 28
AND year = 2020
AND month = 07
AND atm_location LIKE "%Fifer%"
AND transaction_type = "withdraw"))
--check for any outgoing calls the day of the crime
AND phone_number IN
(SELECT caller FROM phone_calls
WHERE day = 28
AND month = 07
AND year = 2020)
--check to license plate for a car exiting within 10 minutes of the crime
AND license_plate IN 
(SELECT license_plate FROM courthouse_security_logs
WHERE day = 28
AND year = 2020
AND month = 07
AND hour = 10
AND activity = "exit"
AND minute BETWEEN 15 AND 25)
--check who took the first flight out of the city
AND passport_number IN
(SELECT passport_number FROM passengers
WHERE flight_id IN
(SELECT id FROM flights
WHERE day BETWEEN 28 AND 30
AND month = 07
AND year = 2020
ORDER BY hour, minute
LIMIT 1));

-- Thief ***
--Crime scene reports
    --# look for reports where year, month, day & street match
        --"Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
        --Interviews were conducted today with three witnesses who 
       -- were present at the time — each of their interview transcripts mentions the courthouse."
    
    -- # search interviews for 7/28/2020 where text mentions courthouse    
        
        -- -"Sometime within ten minutes of the theft, I saw the thief get into a car
        --in the courthouse parking lot and drive away. If you have security
        --footage from the courthouse parking lot, you might want to look for cars
        --that left the parking lot in that time frame." (id 161)
        
            --# find any logs of a car exiting parking garage on 7/28/2020 between 10:15 & 10:25
        
        --"I don't know the thief's name, but it was someone I recognized.
        --Earlier this morning,before I arrived at the courthouse,
        --I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money." (id 162)
            
            --# check atm logs between 6am and 10:15am
        
        --“Pshaw! They did not know how to look.” (id 163)




--select the person who recieved the shortest phone call from ernest (get away call)
SELECT name FROM people
WHERE phone_number IN
(SELECT receiver from phone_calls
WHERE day = 28
AND month = 07
AND year = 2020
AND caller IN
(SELECT phone_number from people
WHERE name = "Ernest")
ORDER BY duration
LIMIT 1);

--find out which flight ernest took and what the destination was
SELECT city FROM airports
WHERE id IN
(SELECT destination_airport_id FROM flights
WHERE id IN
(SELECT flight_id FROM passengers
WHERE passport_number IN
(SELECT passport_number FROM people
WHERE name LIKE "%Ernest%"))
AND day BETWEEN 28 AND 30
AND month = 07
AND year = 2020);







