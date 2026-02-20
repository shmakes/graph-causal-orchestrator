# Causal overlay schema

The causal overlay sits on top of the existing telecom graph. It adds outcome nodes and `CAUSES` edges so we can query "causal paths to churn" (see `specs/examples/churn_investigation.yml`).

## Nodes

- **ChurnOutcome**  
  Represents the outcome "customer churn" for a single customer.  
  - Properties: `customerId` (string, matches `Customer.id`)  
  - One `ChurnOutcome` per churned customer, or one global node; we use **one node per churned customer** so paths are per-customer and we can attach factors to the right outcome.

## Relationships

- **Customer -[:HAS_OUTCOME]-> ChurnOutcome**  
  Links a customer to their churn outcome node. Only created when `Customer.customerStatus = 'Churned'`.

- **(Factor) -[:CAUSES]-> ChurnOutcome**  
  Factor nodes that we consider causal drivers of churn.  
  - **Contract** (existing): `(Contract)-[:CAUSES]->(ChurnOutcome)` for each ChurnOutcome of a customer who has that contract.  
  - **Offer** (existing): `(Offer)-[:CAUSES]->(ChurnOutcome)` for each ChurnOutcome of a customer who had that offer.  
  - Optional: binned tenure or other factor nodes can be added later with the same pattern.

## Node identity for Cypher

- **Customer**: `Customer.id`
- **Contract**: `Contract.name`
- **Offer**: `Offer.name`
- **ChurnOutcome**: we use a composite id `churn:<customerId>` stored as property `id` on `ChurnOutcome` for consistent lookup in causal_kg (e.g. `get_causal_parents(client, "churn:0004-TLHLJ", 1)`).

## Summary

- Existing: `Customer`, `Contract`, `Offer`, `InternetType`, `PaymentMethod`, `City`, etc., with existing relationship types.
- Causal overlay: `ChurnOutcome` nodes (one per churned customer), `HAS_OUTCOME` from Customer to ChurnOutcome, and `CAUSES` from Contract/Offer (and optionally other factors) to ChurnOutcome.
