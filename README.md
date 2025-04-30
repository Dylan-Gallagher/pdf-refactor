# PDF-Refactor

## Intro
This is a tool I made to convert lecture slides in the format
```
<Slide 1 Title>
point 1

<Slide 1 Title>
point 1
point 2

<Slide 1 Title>
point 1
point 2
point 3

<Slide 2 Title>
point 1

<Slide 2 Title>
point 1
point 2

<Slide 2 Title>
point 1
point 2
point 3

...
```

into the format

```
<Slide 1 Title>
point 1
point 2
point 3

<Slide 2 Title>
point 1
point 2
point 3

...
```

It takes only the complete lecture slides, and not the "transition" lecture slides.

This is useful because I can pass my lecture slides into this tool and get out a smaller (non-repeating) pdf. This has many use-cases such as:
- Passing to an AI to explain lecture notes (AI struggled a bit with all the repetition)
- Having a more compact representation, useful for "Control-F"-ing the document.

## Installation Instructions
```bash
pip install -r requirements.txt
python3 pdfrefactor.py "path/to/your/input/slides.pdf"
```
