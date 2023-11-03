# AdaptlyAI

## Inspiration

In an age where online learning is ubiquitous, the limitations of "one-size-fits-all" educational content have become strikingly clear. Our team at Adaptly AI is driven by the conviction that the effectiveness of learning is significantly heightened when it is customized to an individual's unique experiences, preferred styles of explanation, and language. Drawing inspiration from the natural human tendency to use relatable analogies for explaining complex topics, we set out to create an AI that could make every learning experience as intuitive as discussing a hobby.

## About Adaptly AI

Adaptly AI is an innovative application designed to deliver a bespoke educational experience. It attentively listens to users express their personal experiences, hobbies, language of preference for learning, and desired styles of explanation. The application leverages this information to personalize subsequent educational material, drawing on analogies and references from the user's own experiences to ensure that each learning journey is distinctive, customized, and above all, effective.

To achieve this, we've harnessed the power of Google's Speech-to-Text API for converting user's spoken input into text. This textual data is then fed into the sophisticated GPT-4 model, which meticulously analyzes the transcript to distill critical insights about the user's personal experiences, learning preferences, and linguistic choices. Our Flask-based backend orchestrates the processing, while MongoDB dutifully archives the gleaned data for continual enhancement of the learning experience.

In addition to this, we've fine-tuned our video recognition model utilizing the capabilities of OpenCV and TensorFlow to ensure a seamless and interactive learning environment.

## Contributors

- Elijah Umana
- Jason Antwi-Appah
- David Ramirez


##Contributors Elijah Umana, Jason Antwi-Appah, and 
David Ramirez

## Backend
Create Virtual Environment: `python3 -m venv venv`
Activate Virtual Environment: `source venv/bin/activate`
Download dependencies: `pip3 install -r requirements.txt`
Run backend: `python3 app.py`

## Frontend
Install dependencies: `npm install`
Run frontend: `npm start`
