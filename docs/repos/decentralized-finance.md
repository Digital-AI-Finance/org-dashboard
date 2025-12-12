# decentralized-finance

BSc Blockchain, Crypto Economy, and NFTs Course Materials

[View on GitHub](https://github.com/Digital-AI-Finance/decentralized-finance){ .md-button .md-button--primary }


---





## Information

| Property | Value |
|----------|-------|
| Language | TeX |
| Stars | 0 |
| Forks | 0 |
| Watchers | 0 |
| Open Issues | 0 |
| License | No License |
| Created | 2025-12-08 |
| Last Updated | 2025-12-11 |
| Last Push | 2025-12-11 |
| Contributors | 1 |
| Default Branch | master |
| Visibility | public |






## Datasets

This repository includes 1 dataset(s):

| Dataset | Format | Size |
|---------|--------|------|

| [.pdf_hashes.json](https://github.com/Digital-AI-Finance/decentralized-finance/blob/master/.pdf_hashes.json) | .json | 6.64 KB |




## Reproducibility


No specific reproducibility files found.







## Status





- Issues: Enabled
- Wiki: Enabled
- Pages: Enabled

## README

# BSc Blockchain, Crypto Economy & NFTs

A comprehensive course covering blockchain technology, cryptocurrency economics, and non-fungible tokens (NFTs) for Bachelor of Science students.

## Course Overview

This 12-week course (48 lessons, 6 ECTS credits) provides both theoretical understanding and practical skills in distributed ledger technology, smart contracts, decentralized finance (DeFi), and digital asset management. Students engage in hands-on laboratory exercises and complete a semester-long project applying blockchain concepts to real-world scenarios.

### Key Learning Objectives

- Understand blockchain fundamentals, consensus mechanisms, and cryptographic principles
- Develop and deploy smart contracts using Solidity
- Analyze token economics and DeFi protocols
- Evaluate NFT technology and digital asset markets
- Assess regulatory frameworks and security considerations
- Design blockchain-based solutions for business problems

## Repository Structure

### Modules (7 total, 48 lessons)

```
Module_A_Blockchain_Foundations/     (12 lessons)
  - Blockchain basics, hash functions, cryptography
  - Bitcoin protocol, consensus mechanisms
  - Scalability trilemma

Module_B_Ethereum_Smart_Contracts/   (8 lessons)
  - Ethereum architecture, EVM, gas mechanics
  - Solidity programming
  - Token standards (ERC20, ERC721, ERC1155)

Module_C_NFTs_Digital_Assets/        (8 lessons)
  - NFT technology, metadata, IPFS
  - NFT marketplaces and applications
  - Digital art, gaming, real-world asset tokenization

Module_D_Tokenomics/                 (4 lessons)
  - Token economics fundamentals
  - Distribution models, vesting schedules
  - Token classification and valuation

Module_E_DeFi_Ecosystem/             (8 lessons)
  - Decentralized finance overview
  - Automated market makers (Uniswap)
  - Lending protocols, stablecoins
  - Case study: Terra/Luna collapse

Module_F_Advanced_Topics/            (4 lessons)
  - Layer 2 scaling solutions
  - Flash loans and composability
  - Smart contract security

Module_G_Regulation_Future/          (4 lessons)
  - Global regulatory landscape
  - Swiss FINMA and EU MiCA frameworks
  - CBDCs and future trends
```

### Supporting Materials

```
assessments/
  projects/     - Semester project specifications (4 tracks)
  quizzes/      - 5 quizzes covering course material
  rubrics/      - Grading criteria for all assessments

labs/           - 12 hands-on laboratory exercises

charts/         - Visualizations and diagrams
```

## Quick Navigation

### Essential Documents

- **[SYLLABUS.md](SYLLABUS.md)** - Complete course syllabus with schedule, assessment structure, and policies
- **[PROGRESS_TRACKER.md](PROGRESS_TRACKER.md)** - Development status for all 48 lessons and materials

### Course Schedule (12 Weeks)

| Week | Module | Topics | Lab |
|------|--------|--------|-----|
| 1 | A | What is Blockchain, DLT, Hash Functions | Hash Experiments |
| 2 | A | Cryptography, Bitcoin, Proof of Work | Wallet Setup |
| 3 | A | Proof of Stake, Consensus, Scalability | Block Explorer |
| 4 | B | Ethereum, EVM, Gas, Solidity | Contract Interaction |
| 5 | B | ERC20, ERC721/1155, Token Lifecycle | Token Deployment |
| 6 | C | NFT Technology, Metadata, Marketplaces | OpenSea Analysis |
| 7 | C | Digital Art, Gaming, RWA Tokenization | NFT Valuation |
| 8 | D | Token Economics, Distribution, Valuation | Tokenomics Analysis |
| 9 | E | DeFi Intro, AMMs, Uniswap | Testnet Swap |
| 10 | E | Lending, Stablecoins, Terra/Luna | Testnet Lending |
| 11 | F | Layer 2, Flash Loans, Security | Security Audit |
| 12 | G | Regulation, FINMA/MiCA, CBDCs | Course Synthesis |

## Assessment Structure

### Grade Breakdown
- **Semester Project:** 70%
- **Quizzes:** 10% (5 quizzes)
- **Laboratory Exercises:** 15% (best 10 of 12)
- **Class Participation:** 5%

### Project Tracks (Choose 1)

1. **Token Economy Design** - Design and implement a complete tokenomics model
2. **NFT Platform Development** - Deploy NFT collection with utility features
3. **DeFi Protocol Analysis** - Deep analysis and simulation of DeFi protocol
4. **Supply Chain Solution** - Blockchain-based supply chain tracking system

## Prerequisites

### Knowledge Prerequisites
- Basic programming knowledge (Python or similar)
- Understanding of basic economic principles
- Familiarity with web technologies (helpful but not required)

### Required Tools
- **Cryptocurrency Wallet:** MetaMask (browser extension)
- **Development Environment:** Remix IDE, Hardhat or Foundry, VS Code
- **Blockchain Explorers:** Etherscan, Blockchain.com
- **Testnet Access:** Sepolia/Goerli ETH faucets
- **Data Analysis:** Python (pandas, web3.py, matplotlib)

## How to Use This Repository

### For Instructors

1. **Review the syllabus** - [SYLLABUS.md](SYLLABUS.md) contains complete course structure
2. **Check lesson materials** - Navigate to individual lesson folders for slides and charts
3. **Prepare labs** - Review lab guides in the `labs/` directory
4. **Customize assessments** - Adapt project specifications and quizzes in `assessments/`
5. **Track progress** - Use [PROGRESS_TRACKER.md](PROGRESS_TRACKER.md) to monitor development

### For Students

1. **Follow the weekly schedule** - See syllabus for lesson sequence
2. **Complete labs on time** - 12 hands-on exercises throughout the semester
3. **Prepare for quizzes** - 5 quizzes covering 2-week blocks
4. **Choose project track early** - Team formation by Week 3
5. **Use testnet only** - Never use real cryptocurrency for exercises

### For Content Developers

1. **Check PROGRESS_TRACKER.md** - See which lessons need development
2. **Follow naming conventions** - Use `YYYYMMDD_HHMM_` prefix for .tex files
3. **Use Python for charts** - No TikZ; standalone Python scripts in chart folders
4. **Update tracking files** - Mark lessons as complete in PROGRESS_TRACKER.md
5. **Compile and verify PDFs** - Ensure all materials render correctly

## Technical Specifications

### Slide Format
- **Framework:** LaTeX Beamer
- **Theme:** Madrid
- **Font Size:** 8pt
- **Aspect Ratio:** 16:9
- **Template:** `template_beamer_final.tex`

### Chart Generation
- **Language:** Python (matplotlib, seaborn)
- **Format:** PDF output
- **Organization:** One folder per chart with script and output
- **Naming:** Content-based names (e.g., `bitcoin_network_growth/`)

### File Versioning
- All .tex files prefixed with timestamp: `YYYYMMDD_HHMM_filename.tex`
- Previous versions stored in `previous/` subdirectories
- PDFs compiled with full output path logging

## Development Status

### Current Progress (as of 2025-12-09)

| Category | Completed | Total | Progress |
|----------|-----------|-------|----------|
| Lessons | 48 | 48 | 100% |
| Lab Guides | 11 | 11 | 100% |
| Charts | 8 | 8 | 100% |
| Quizzes | 6 | 6 | 100% |
| Assessments | Complete | - | 100% |

**Latest Updates:**
- All 48 lesson slides created and compiled to PDF
- All 11 lab guides completed
- 8 visualization charts generated (Python/matplotlib)
- 6 quizzes with answer keys
- Project guide with 4 tracks, grading rubrics, milestone templates
- GitHub Pages deployed at https://digital-ai-finance.github.io/decentralized-finance

See [PROGRESS_TRACKER.md](PROGRESS_TRACKER.md) for detailed status.

## Course Policies

### Academic Integrity
- All work must be original with proper attribution
- AI tool usage (ChatGPT, Copilot) must be disclosed
- Plagiarism results in automatic course failure

### Safety & Security
- **NEVER use real cryptocurrency for learning exercises**
- Always use testnets (Sepolia, Goerli)
- Never share private keys or seed phrases
- Be cautious of phishing attempts

### Collaboration
- Labs: Individual work, discussion permitted
- Quizzes: Individual work, no collaboration
- Project: Team collaboration expected, individual contributions documented

## Resources

### Required Readings
- Antonopoulos, A. M. (2017). *Mastering Bitcoin* (2nd ed.)
- Antonopoulos, A. M., & Wood, G. (2018). *Mastering Ethereum*
- Selected academic papers (provided weekly)

### Recommended Platforms
- Ethereum.org documentation
- Solidity documentation
- DeFi Llama (protocol analytics)
- OpenZeppelin (smart contract library)

### Community & Support
- Course discussion forum (link TBD)
- Office hours (schedule TBD)
- Teaching assistant lab hours (schedule TBD)

## Contact Information

**Instructor:** [Name]
**Email:** [Email]
**Office:** [Location]
**Office Hours:** [Schedule]

**Teaching Assistant:** [Name]
**Email:** [Email]
**Lab Hours:** [Schedule]

## License & Disclaimer

This course is for educational purposes only. Nothing in this course constitutes financial or investment advice. Cryptocurrency and blockchain technologies involve significant risks. Students are responsible for complying with all applicable laws and regulations in their jurisdiction.

---

**Course ID:** [TBD]
**Department:** [TBD]
**Institution:** [TBD]
**Last Updated:** December 2025
**Version:** 1.0
