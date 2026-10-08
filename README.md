# BEAMS

Brand Exposure Analytics and Metrics System.

## Abstract

Sports sponsorship has become one of the most valuable forms of brand marketing, yet its effectiveness remains difficult to measure with precision. Existing computer vision based analytics systems quantify visibility through surface level exposure metrics, treating every appearance of a logo as equally valuable regardless of how it was actually perceived. However, exposure alone does not determine impact, viewer attention does, so a prominent logo that fails to draw the eye contributes far less to brand value than one that briefly but genuinely captures attention. This project addresses that gap by proposing a sponsorship analytics system that combines automated logo detection across sports broadcast footage with an attention aware visibility scoring mechanism, producing a more accurate and perceptually grounded measure of sponsorship value. Findings are delivered through a natural language reporting layer, allowing sponsors and marketing teams to interpret complex visibility data without technical expertise.

## Installation

Run this command to install the project:

```bash
git clone "https://github.com/ElvinAlapatt/BEAMS.git"
```
```bash
cd BEAMS
```
```bash
uv sync
```

## Usage

Here is a quick example of how to use it:

Command to run the backend
```bash
uv run uvicorn backend.main:app --reload
```
Command to run the frontend
```bash
cd frontend
```
```bash
streamlit run app.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
