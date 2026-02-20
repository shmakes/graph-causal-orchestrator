#!/usr/bin/env python3
"""
Import local IBM Telco data into Neo4j:
  - scripts/telecom_customer_churn.csv   -> Customer nodes + Contract, Offer, City, etc.
  - scripts/telecom_zipcode_population.csv -> ZipCode nodes
  - scripts/telecom_data_dictionary.csv   -> Table + Field nodes (metadata)

Run from project root: uv run python scripts/import_telecom_data.py
"""

import csv
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
os.chdir(PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

from neo4j import GraphDatabase


def load_settings():
    from config.settings import get_settings
    return get_settings()


def strip_row(r):
    return {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in r.items()}


def safe_float(s):
    if s is None or (isinstance(s, str) and not s.strip()):
        return None
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def safe_int(s):
    if s is None or (isinstance(s, str) and not s.strip()):
        return None
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return None


def load_zipcodes(driver, path: str) -> int:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with driver.session() as session:
        session.run("MATCH (z:ZipCode) DETACH DELETE z")
        for r in rows:
            r = strip_row(r)
            zip_code = (r.get("Zip Code") or "").strip()
            pop = safe_int(r.get("Population", ""))
            if not zip_code:
                continue
            session.run(
                "MERGE (z:ZipCode {zipCode: $zipCode}) SET z.population = $population",
                zipCode=zip_code,
                population=pop,
            )
    return len(rows)


def load_customers(driver, path: str) -> int:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return 0

    with driver.session() as session:
        session.run("MATCH (c:Customer) DETACH DELETE c")
        session.run("MATCH (n:Contract) DETACH DELETE n")
        session.run("MATCH (n:Offer) DETACH DELETE n")
        session.run("MATCH (n:InternetType) DETACH DELETE n")
        session.run("MATCH (n:PaymentMethod) DETACH DELETE n")
        session.run("MATCH (n:City) DETACH DELETE n")

        for i, raw in enumerate(rows):
            r = strip_row(raw)
            cid = (r.get("Customer ID") or "").strip()
            if not cid:
                continue

            session.run(
                """
                MERGE (c:Customer {id: $id})
                SET c.gender = $gender, c.age = $age, c.married = $married,
                    c.numberOfDependents = $numberOfDependents, c.city = $city,
                    c.zipCode = $zipCode, c.latitude = $latitude, c.longitude = $longitude,
                    c.numberOfReferrals = $numberOfReferrals, c.tenureMonths = $tenureMonths,
                    c.offer = $offer, c.phoneService = $phoneService,
                    c.avgMonthlyLongDistanceCharges = $avgMonthlyLongDistanceCharges,
                    c.multipleLines = $multipleLines, c.internetService = $internetService,
                    c.internetType = $internetType, c.avgMonthlyGBDownload = $avgMonthlyGBDownload,
                    c.onlineSecurity = $onlineSecurity, c.onlineBackup = $onlineBackup,
                    c.deviceProtectionPlan = $deviceProtectionPlan,
                    c.premiumTechSupport = $premiumTechSupport,
                    c.streamingTV = $streamingTV, c.streamingMovies = $streamingMovies,
                    c.streamingMusic = $streamingMusic, c.unlimitedData = $unlimitedData,
                    c.contract = $contract, c.paperlessBilling = $paperlessBilling,
                    c.paymentMethod = $paymentMethod, c.monthlyCharge = $monthlyCharge,
                    c.totalCharges = $totalCharges, c.totalRefunds = $totalRefunds,
                    c.totalExtraDataCharges = $totalExtraDataCharges,
                    c.totalLongDistanceCharges = $totalLongDistanceCharges,
                    c.totalRevenue = $totalRevenue, c.customerStatus = $customerStatus,
                    c.churnCategory = $churnCategory, c.churnReason = $churnReason
                """,
                id=cid,
                gender=r.get("Gender"),
                age=safe_int(r.get("Age")),
                married=r.get("Married"),
                numberOfDependents=safe_int(r.get("Number of Dependents")),
                city=r.get("City"),
                zipCode=r.get("Zip Code"),
                latitude=safe_float(r.get("Latitude")),
                longitude=safe_float(r.get("Longitude")),
                numberOfReferrals=safe_int(r.get("Number of Referrals")),
                tenureMonths=safe_int(r.get("Tenure in Months")),
                offer=r.get("Offer") or None,
                phoneService=r.get("Phone Service"),
                avgMonthlyLongDistanceCharges=safe_float(r.get("Avg Monthly Long Distance Charges")),
                multipleLines=r.get("Multiple Lines"),
                internetService=r.get("Internet Service"),
                internetType=r.get("Internet Type") or None,
                avgMonthlyGBDownload=safe_float(r.get("Avg Monthly GB Download")),
                onlineSecurity=r.get("Online Security"),
                onlineBackup=r.get("Online Backup"),
                deviceProtectionPlan=r.get("Device Protection Plan"),
                premiumTechSupport=r.get("Premium Tech Support"),
                streamingTV=r.get("Streaming TV"),
                streamingMovies=r.get("Streaming Movies"),
                streamingMusic=r.get("Streaming Music"),
                unlimitedData=r.get("Unlimited Data"),
                contract=r.get("Contract"),
                paperlessBilling=r.get("Paperless Billing"),
                paymentMethod=r.get("Payment Method"),
                monthlyCharge=safe_float(r.get("Monthly Charge")),
                totalCharges=safe_float(r.get("Total Charges")),
                totalRefunds=safe_float(r.get("Total Refunds")),
                totalExtraDataCharges=safe_float(r.get("Total Extra Data Charges")),
                totalLongDistanceCharges=safe_float(r.get("Total Long Distance Charges")),
                totalRevenue=safe_float(r.get("Total Revenue")),
                customerStatus=r.get("Customer Status"),
                churnCategory=r.get("Churn Category") or None,
                churnReason=r.get("Churn Reason") or None,
            )

            zip_code = (r.get("Zip Code") or "").strip()
            if zip_code:
                session.run(
                    "MERGE (z:ZipCode {zipCode: $zipCode}) MERGE (c:Customer {id: $cid}) MERGE (c)-[:IN_ZIPCODE]->(z)",
                    zipCode=zip_code,
                    cid=cid,
                )

            contract = (r.get("Contract") or "").strip()
            if contract:
                session.run(
                    "MERGE (ct:Contract {name: $name}) MERGE (c:Customer {id: $cid}) MERGE (c)-[:HAS_CONTRACT]->(ct)",
                    name=contract,
                    cid=cid,
                )

            offer = (r.get("Offer") or "").strip()
            if offer and offer.lower() != "none":
                session.run(
                    "MERGE (o:Offer {name: $name}) MERGE (c:Customer {id: $cid}) MERGE (c)-[:HAS_OFFER]->(o)",
                    name=offer,
                    cid=cid,
                )

            internet_type = (r.get("Internet Type") or "").strip()
            if internet_type:
                session.run(
                    "MERGE (it:InternetType {name: $name}) MERGE (c:Customer {id: $cid}) MERGE (c)-[:HAS_INTERNET_TYPE]->(it)",
                    name=internet_type,
                    cid=cid,
                )

            payment = (r.get("Payment Method") or "").strip()
            if payment:
                session.run(
                    "MERGE (pm:PaymentMethod {name: $name}) MERGE (c:Customer {id: $cid}) MERGE (c)-[:HAS_PAYMENT_METHOD]->(pm)",
                    name=payment,
                    cid=cid,
                )

            city = (r.get("City") or "").strip()
            if city:
                session.run(
                    "MERGE (city:City {name: $name}) MERGE (c:Customer {id: $cid}) MERGE (c)-[:IN_CITY]->(city)",
                    name=city,
                    cid=cid,
                )

            if (i + 1) % 1000 == 0:
                print(f"  Customers: {i + 1}...")

    return len(rows)


def load_data_dictionary(driver, path: str) -> int:
    # Data dictionary often uses Windows encoding (CP1252); 0x92 = right single quote
    try:
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except UnicodeDecodeError:
        with open(path, newline="", encoding="cp1252") as f:
            rows = list(csv.DictReader(f))
    with driver.session() as session:
        session.run("MATCH (t:Table) DETACH DELETE t")
        session.run("MATCH (f:Field) DETACH DELETE f")
        for r in rows:
            r = strip_row(r)
            table = (r.get("Table") or "").strip()
            field = (r.get("Field") or "").strip()
            desc = (r.get("Description") or "").strip()
            if not table or not field:
                continue
            session.run(
                """
                MERGE (t:Table {name: $table})
                MERGE (f:Field {name: $field, tableName: $table})
                SET f.description = $description
                MERGE (t)-[:HAS_FIELD]->(f)
                """,
                table=table,
                field=field,
                description=desc or None,
            )
    return len(rows)


def main():
    settings = load_settings()
    base = SCRIPT_DIR
    churn_path = os.path.join(base, "telecom_customer_churn.csv")
    zip_path = os.path.join(base, "telecom_zipcode_population.csv")
    dict_path = os.path.join(base, "telecom_data_dictionary.csv")

    for p in (churn_path, zip_path, dict_path):
        if not os.path.isfile(p):
            print(f"Missing: {p}")
            sys.exit(1)

    print(f"Connecting to {settings.neo4j_uri} ...")
    driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )

    try:
        print("Loading zipcode population...")
        nz = load_zipcodes(driver, zip_path)
        print(f"  ZipCode nodes: {nz}")

        print("Loading customer churn...")
        nc = load_customers(driver, churn_path)
        print(f"  Customer nodes: {nc}")

        print("Loading data dictionary...")
        nd = load_data_dictionary(driver, dict_path)
        print(f"  Table/Field rows: {nd}")
    finally:
        driver.close()

    print("Done. All three datasets imported into Neo4j.")


if __name__ == "__main__":
    main()
