# Self-Sovereign Identity — Semantic Framework and Evaluation Resources

**Author:** Cristian Lepore  
**Affiliation:** Université de Toulouse, IRIT Laboratory  
**Thesis:** *A Semantic Framework for Defining and Assessing e-Identity Management Ecosystems Based on Self-Sovereign Identity Principles* (Ph.D. Candidate, 2025)  

---

## 🧭 Overview

This repository provides the **ontologies, principles, scripts, and datasets** developed during the doctoral research on **Self-Sovereign Identity (SSI)**.  
They implement and validate a **semantic framework** for modeling and evaluating **digital identity ecosystems** according to SSI principles and the Trust over IP (ToIP) stack.

All materials are structured to ensure **transparency**, **reproducibility**, and **reuse** for academic or applied research.

---

## 🗂️ Repository Structure (Grouped by Topic)

### 🧩 Theoretical Foundations

#### 1. Kernel Theories (KT)
**File:** [`Kernel_Theories/kernel_theories.md`](https://github.com/cristianlepore/Self-Sovereign_Identity/blob/main/kernel_theories/kernel_theories.md)

Contains the **foundational theories** supporting the semantic and evaluative framework.  
Each Kernel Theory corresponds to one or more **Design Principles (DP)** from the ToIP and SSI paradigms.

Schema used:
> **Design Principle → Objective (Why) → Mechanism (How) → Conditions (Where/When) → Kernel Theories → How Obtained**

Representative examples:
- **End-to-End Principle** — Saltzer, Reed & Clark (1984)  
- **Modularity & Layering** — Baldwin & Clark (2000)  
- **Public Key Cryptography Theory** — Diffie & Hellman (1976); Rivest et al. (1978)  
- **Privacy by Design** — Cavoukian (2009)  
- **Relational Theory of Trust** — Hardin (2002)  
- **Value Sensitive Design / Responsible Innovation** — Friedman et al. (2002); Stilgoe et al. (2013)

These Kernel Theories form the **epistemic backbone** of the ontology, grounding the model in rigorous interdisciplinary theory.

---

### 🧱 SSI Principles and Conceptual Model

#### 2. Principles of Self-Sovereign Identity
**File:** [`principles_of_ssi.md`](https://github.com/cristianlepore/Self-Sovereign_Identity/blob/main/principles_of_ssi.md)

A harmonized list of **SSI principles** derived from a systematic literature review and expert validation.  
Each principle includes:
- Definition  
- Source references  
- Assigned category  

#### 3. Principles and Categories Table
**Link:** [Principles_and_categories.html](https://cristianlepore.github.io/Self-Sovereign_Identity/Principles_and_categories.html)

Interactive HTML visualization showing the **clustering of SSI principles** into thematic domains (corresponding to Table 5.3 in the thesis).

#### 4. Final List of SSI Principles
**Path:** [`/definition_of_principles.md`](https://github.com/cristianlepore/Self-Sovereign_Identity/blob/main/definition_of_principles.md)

Validated and consolidated list of principles used in the evaluation of **case studies** (eIDAS, Sovrin, Bhutan NDI).

---

### 🧠 Ontologies

#### 5. Reference Ontology (ToIP)
**Path:** [`/ontologie/toip`](https://github.com/cristianlepore/Self-Sovereign_Identity/tree/main/ontologies/toip)

This folder contains the **Sample Ontology** developed in RDF/OWL, which implements the **Semantic Framework** proposed in the thesis.  
It models the **four-layer Trust over IP (ToIP) architecture** — *Technology*, *Utility*, *Governance*, and *Ecosystem* — through formal classes, properties, and relationships that link **technical entities** to **normative and ethical values**.  

The ontology serves as the **conceptual backbone** of the framework, enabling semantic reasoning, interoperability, and the evaluation of digital identity ecosystems according to **Self-Sovereign Identity (SSI)** principles.

#### 6. Ontologies for Case Studies
**Path:** [`/ontologies`](https://github.com/cristianlepore/Self-Sovereign_Identity/tree/main/ontologies)

Contains ontology instances for real-world identity systems:
- eIDAS  
- Sovrin  
- PKIX
- uPort  
- Bhutan NDI  

These are used to **test and compare** systems within the semantic evaluation model.

---

### 🧮 Analytical and Computational Tools

#### 7. Semantic Value Ontology (SVO) — Python Scripts
**Path:** [`/`](https://github.com/cristianlepore/Self-Sovereign_Identity/tree/main)

Python scripts implementing the **Semantic Value Ontology (SVO)**, which links architectural components to normative values.  
Used to generate ontology instances and map principles to entities.

#### 8. Clustering and Dimensionality Reduction
**Path:** [`/`](https://github.com/cristianlepore/Self-Sovereign_Identity/tree/main)

Scripts for:
- **K-Means clustering**
- **t-SNE dimensionality reduction**

Used to identify conceptual clusters of SSI principles, as described in **Appendix B** of the thesis.

#### 9. SPARQL Queries
**File:** [`queries/sparql.py`](https://github.com/cristianlepore/Self-Sovereign_Identity/blob/main/queries/sparql.py)

Contains **SPARQL queries** used in the *Principle Engine* to extract, compare, and score relationships between principles, indicators, and system components.

---

### ⚙️ 10. Libraries and Dependencies

**File:** [`libraries.md`](https://github.com/cristianlepore/Self-Sovereign_Identity/blob/main/libraries.md)

This section provides a dependency map of all Python scripts used across the repository.  
Most scripts rely on **NumPy** for numerical computation and **Matplotlib** for data visualization, while ontology-related scripts additionally use **Owlready2** for semantic reasoning.

#### 🧩 Core Libraries
- **NumPy (`np`)** — numerical operations, matrix manipulation, statistical computation  
- **Matplotlib (`plt`, `ax`)** — plotting utilities for visual analysis  
- **Owlready2 (`get_ontology`, `sync_reasoner`, `URIRef`, `rdf_graph`)** — ontology management and reasoning in RDF/OWL

---

### 📚 BibTeX

```bibtex
@phdthesis{lepore2025ssi,
  author    = {Cristian Lepore},
  title     = {A Semantic Framework for Defining and Assessing e-Identity Management Ecosystems Based on Self-Sovereign Identity Principles},
  school    = {Université de Toulouse},
  year      = {2025},
  address   = {Toulouse, France}
}
