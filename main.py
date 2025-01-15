class Event:
    def __init__(self, name, payload):
        self.name = name
        self.payload = payload

class ApplicationSubmittedEvent(Event):
     def __init__(self, applicant_name, job_title):
        super().__init__("application_submitted", {"applicant_name": applicant_name, "job_title": job_title})

class ApplicationReviewedEvent(Event):
    def __init__(self, applicant_name, job_title, is_accepted):
        super().__init__("application_reviewed", {"applicant_name": applicant_name,"job_title": job_title,"is_accepted": is_accepted})

class EventQueue:
    def __init__(self):
        self.queue = []
        self.handlers = {}

    def emit(self, event):
        self.queue.append(event)
        print(f"Event '{event.name}' emitted!")

    def register_handler(self, event_name, handler):
        self.handlers[event_name] = handler

    def process_events(self):
        while self.queue:
            event = self.queue.pop(0)
            if event.name in self.handlers:
                handler = self.handlers[event.name]
                handler(event)
            else:
                print(f"No handler registered for event: {event.name}")
                
communication_queue = EventQueue()


class Applicant:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def apply_for_job(self, job_title):
        event = ApplicationSubmittedEvent(self.name, job_title)
        communication_queue.emit(event)


class Company:
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def handle_application_submission(self, event):
        print(f"Processing job application for {event.payload['applicant_name']} for the position {event.payload['job_title']}.")
        # For demonstration, we accept all applications
        is_accepted = True
        review_event = ApplicationReviewedEvent(event.payload['applicant_name'], event.payload['job_title'], is_accepted)
        communication_queue.emit(review_event)

    def handle_application_review(self, event):
        status = "accepted" if event.payload['is_accepted'] else "rejected"
        print(f"Application for {event.payload['applicant_name']} for the position {event.payload['job_title']} is {status}.")
