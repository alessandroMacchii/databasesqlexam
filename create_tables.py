import psycopg2

conn = psycopg2.connect(
    host="db", 
    database="f1db",
    user="postgres",
    password="password",
    port="5432"
)

with conn: 
    with conn.cursor() as cur:
        #non mettiamo driver ref perché è come se fosse un cognome univoco
        #non mettiamo neanche constructor ref per la stessa ragione, idem circuitref
        #time result (tempo di fine gara) tolto perché abbiamo i milliseconds e possiamo calcolarlo
        
        cur.execute("DROP TABLE IF EXISTS results CASCADE;")
        cur.execute("DROP TABLE IF EXISTS races CASCADE;")
        cur.execute("DROP TABLE IF EXISTS drivers CASCADE;")
        cur.execute("DROP TABLE IF EXISTS constructors CASCADE;")
        cur.execute("DROP TABLE IF EXISTS circuits CASCADE;")
        cur.execute("DROP TABLE IF EXISTS status CASCADE;")

        cur.execute("""
        CREATE TABLE drivers 
            (driverid SERIAL PRIMARY KEY,
            name TEXT NOT NULL, 
            surname TEXT NOT NULL,
            number INT CHECK(number>=1),
            code TEXT CHECK(length(code) = 3 AND code = UPPER(code)),
            dob DATE,
            nationality TEXT,
            url TEXT
                     );
                     """)

        cur.execute("""
        CREATE TABLE constructors (
                     constructorid SERIAL PRIMARY KEY,
                     name TEXT NOT NULL, 
                     nationality TEXT,
                     url TEXT
                     );
                     """)
        
        cur.execute("""
        CREATE TABLE circuits (
            circuitid SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT,
            country TEXT,
            lat REAL,
            lng REAL,
            alt REAL,
            url TEXT
        );
        """)
        
        cur.execute("""
        CREATE TABLE status (
        statusid SERIAL PRIMARY KEY,
        status TEXT NOT NULL
                     );
                     """)
        
        cur.execute("""
        CREATE TABLE races (
        raceid SERIAL PRIMARY KEY,
        year INTEGER NOT NULL,
        round INTEGER NOT NULL,
        circuitid INTEGER,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        time_race TEXT,
        url TEXT,
        quali_date TEXT,
        quali_time TEXT,
        sprint_date TEXT,
        sprint_time TEXT,
        FOREIGN KEY (circuitid) REFERENCES circuits(circuitid)
        );
        """)

        cur.execute("""
        CREATE TABLE results (
        resultid SERIAL PRIMARY KEY,
        raceid INTEGER,
        driverid INTEGER,
        constructorid INTEGER,
        statusid INTEGER,
        number INTEGER,
        grid INTEGER,
        position INTEGER,
        positionText TEXT,
        positionOrder INTEGER NOT NULL,
        points REAL,
        laps INTEGER,
        milliseconds INTEGER,
        fastestLap INTEGER,
        rank INTEGER,
        fastestLapTime TEXT,
        fastestLapSpeed REAL,
        FOREIGN KEY (raceid) REFERENCES races(raceid) ON DELETE CASCADE,
        FOREIGN KEY (driverid) REFERENCES drivers(driverid) ON DELETE CASCADE,
        FOREIGN KEY (constructorid) REFERENCES constructors(constructorid) ON DELETE SET NULL,
        FOREIGN KEY (statusid) REFERENCES status(statusid) ON DELETE SET NULL
            );
                     """)
        
        print ("tables created successfully")