"""
1)
Fever?
    Yes:
        Body Aches?
            Yes:
                Chills?
                    Yes: Likely Influenza (Flu)
                    No: Possible Cold or Other Infection
            No:
                Headache?
                    Yes: Possible Sinus Infection or Other Infection
                    No: Possible Cold or Other Infection
    No:
        Cough?
            Yes:
                Sore Throat?
                Yes: Likely Cold
                No: Possible Allergies or Other Respiratory Issue
            No:
                Runny Nose?
                    Yes: Possible Allergies or Cold
                    No:
                        Vomiting or Diarrhea?
                            Yes: Possible Gastroenteritis (Stomach Flu)
                            No: Consider other causes or consult a doctor

2)
Tree 2: Musculoskeletal Pain

Primary Concern?
    Joint Pain:
        Specific Joint Affected?
            Knee:
                Injury?
                    Yes: Possible Sprain/Strain
                    No: Possible Osteoarthritis or Rheumatoid Arthritis
            Multiple Joints:
                Morning Stiffness?
                    Yes: Possible Rheumatoid Arthritis
                    No: Possible Osteoarthritis or Lupus
    Muscle Pain:
        After Activity?
            Yes: Possible Muscle Strain
            No:
                Fever/Rash?
                    Yes: Consult a doctor (Possible infection)
                    No: Consider other causes

3)
Tree 3: Mental Health (Simplified)

Primary Concern?
    Feeling Down/Sad:
        Loss of Interest in Activities?
            Yes: Possible Depression
            No: Consider other causes or consult a mental health professional
    Excessive Worry:
        Difficulty Controlling Worry?
            Yes: Possible Anxiety Disorder
            No: Consider other causes or consult a mental health professional
    Sleep Problems:
        Difficulty Falling/Staying Asleep?
            Yes: Possible Insomnia or other sleep disorder. Consider consulting a doctor.
            No: Consider other causes
"""