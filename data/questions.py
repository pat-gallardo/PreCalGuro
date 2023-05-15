import pyrebase
import os
import json
import random

# #dummyemail@gmail.com
# #thisispass
# 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
firebaseConfig = {
  "apiKey": "AIzaSyDyihbb440Vb2o0CIMINI_UfQLRln0uvXs",
  "authDomain": "mathguro-46712.firebaseapp.com",
  "databaseURL": "https://mathguro-46712-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "mathguro-46712",
  "storageBucket": "mathguro-46712.appspot.com",
  "messagingSenderId": "24039260333",
  "appId": "1:24039260333:web:673adf358560ef3cbe4624",
  "measurementId": "G-YP2867V22T"
}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()
db=firebase.database()

class display_random_question():
    def random_questions(list_of_quest):
        displayed_questions = (random.sample(list_of_quest, 5))
        disp = []
        for display in range(len(displayed_questions)):
            disp.append(displayed_questions[display])
        return disp[0], disp[1], disp[2], disp[3], disp[4]
    def random_questions_2(list_of_quest):
        displayed_questions = (random.sample(list_of_quest, 10))
        disp = []
        for display in range(len(displayed_questions)):
            disp.append(displayed_questions[display])
        return disp[0], disp[1], disp[2], disp[3], disp[4], disp[5], disp[6], disp[7], disp[8], disp[9]
    def get_scores_for_pre(gathered_random_question):
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(circle)
        circle_questions = db.child("precal_questions").child("pre-assess").child("circleQuestion").get()
        parabola_questions = db.child("precal_questions").child("pre-assess").child("parabolaQuestion").get()
        ellipse_questions = db.child("precal_questions").child("pre-assess").child("ellipseQuestion").get()
        hyperbola_questions = db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").get()
        substitution_questions = db.child("precal_questions").child("pre-assess").child("substitutionQuestion").get()
        elimination_questions = db.child("precal_questions").child("pre-assess").child("eliminationQuestion").get()

        for circle in circle_questions.each():
            if circle.val(["circle_1_question"]) == gathered_random_question:
                answerScore = (circle.val()["answerScore"])
                answerId = (circle.val()["answerId"])
                solutionScore = (circle.val()["solutionScore"])
                solutionId = (circle.val()["solutionId"])

        for parabola in parabola_questions.each():
            if parabola.val(["parabola_question"]) == gathered_random_question:
                answerScore = (parabola.val()["answerScore"])
                answerId = (parabola.val()["answerId"])
                solutionScore = (parabola.val()["solutionScore"])
                solutionId = (parabola.val()["solutionId"])
            
        for ellipse in ellipse_questions.each():
            if parabola.val(["ellipse_question"]) == gathered_random_question:
                answerScore = (ellipse.val()["answerScore"])
                answerId = (ellipse.val()["answerId"])
                solutionScore = (ellipse.val()["solutionScore"])
                solutionId = (ellipse.val()["solutionId"])

        for hyperbola in hyperbola_questions.each():
            if hyperbola.val(["hyperbola _question"]) == gathered_random_question:
                answerScore = (hyperbola.val()["answerScore"])
                answerId = (hyperbola.val()["answerId"])
                solutionScore = (hyperbola.val()["solutionScore"])
                solutionId = (hyperbola.val()["solutionId"])

        for subs in substitution_questions.each():
            if subs.val(["substitution_question"]) == gathered_random_question:
                answerScore = (subs.val()["answerScore"])
                answerId = (subs.val()["answerId"])
                solutionScore = (subs.val()["solutionScore"])
                solutionId = (subs.val()["solutionId"])

        for elim in elimination_questions.each():
            if elim.val(["elimination_question"]) == gathered_random_question:
                answerScore = (elim.val()["answerScore"])
                answerId = (elim.val()["answerId"])
                solutionScore = (elim.val()["solutionScore"])
                solutionId = (elim.val()["solutionId"])

        return answerScore, answerId, solutionScore, solutionId
    def get_scores_for_post(gathered_random_question):
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(circle)
        circle_questions = db.child("precal_questions").child("post-assess").child("circleQuestion").get()
        parabola_questions = db.child("precal_questions").child("post-assess").child("parabolaQuestion").get()
        ellipse_questions = db.child("precal_questions").child("post-assess").child("ellipseQuestion").get()
        hyperbola_questions = db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").get()
        substitution_questions = db.child("precal_questions").child("post-assess").child("substitutionQuestion").get()
        elimination_questions = db.child("precal_questions").child("post-assess").child("eliminationQuestion").get()

        for circle in circle_questions.each():
            if circle.val(["circle_1_question"]) == gathered_random_question:
                answerScore = (circle.val()["answerScore"])
                answerId = (circle.val()["answerId"])
                solutionScore = (circle.val()["solutionScore"])
                solutionId = (circle.val()["solutionId"])

        for parabola in parabola_questions.each():
            if parabola.val(["parabola_question"]) == gathered_random_question:
                answerScore = (parabola.val()["answerScore"])
                answerId = (parabola.val()["answerId"])
                solutionScore = (parabola.val()["solutionScore"])
                solutionId = (parabola.val()["solutionId"])
            
        for ellipse in ellipse_questions.each():
            if parabola.val(["ellipse_question"]) == gathered_random_question:
                answerScore = (ellipse.val()["answerScore"])
                answerId = (ellipse.val()["answerId"])
                solutionScore = (ellipse.val()["solutionScore"])
                solutionId = (ellipse.val()["solutionId"])

        for hyperbola in hyperbola_questions.each():
            if hyperbola.val(["hyperbola _question"]) == gathered_random_question:
                answerScore = (hyperbola.val()["answerScore"])
                answerId = (hyperbola.val()["answerId"])
                solutionScore = (hyperbola.val()["solutionScore"])
                solutionId = (hyperbola.val()["solutionId"])

        for subs in substitution_questions.each():
            if subs.val(["substitution_question"]) == gathered_random_question:
                answerScore = (subs.val()["answerScore"])
                answerId = (subs.val()["answerId"])
                solutionScore = (subs.val()["solutionScore"])
                solutionId = (subs.val()["solutionId"])

        for elim in elimination_questions.each():
            if elim.val(["elimination_question"]) == gathered_random_question:
                answerScore = (elim.val()["answerScore"])
                answerId = (elim.val()["answerId"])
                solutionScore = (elim.val()["solutionScore"])
                solutionId = (elim.val()["solutionId"])

        return answerScore, answerId, solutionScore, solutionId
    
    def get_scores_for_unit1(gathered_random_question):
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(circle)
        circle_questions = db.child("precal_questions").child("lesson1").child("circleQuestion").get()
        parabola_questions = db.child("precal_questions").child("lesson1").child("parabolaQuestion").get()
        ellipse_questions = db.child("precal_questions").child("lesson1").child("ellipseQuestion").get()
        hyperbola_questions = db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").get()

        for circle in circle_questions.each():
            if circle.val(["circle_1_question"]) == gathered_random_question:
                answerScore = (circle.val()["answerScore"])
                answerId = (circle.val()["answerId"])
                solutionScore = (circle.val()["solutionScore"])
                solutionId = (circle.val()["solutionId"])

        for parabola in parabola_questions.each():
            if parabola.val(["parabola_question"]) == gathered_random_question:
                answerScore = (parabola.val()["answerScore"])
                answerId = (parabola.val()["answerId"])
                solutionScore = (parabola.val()["solutionScore"])
                solutionId = (parabola.val()["solutionId"])
            
        for ellipse in ellipse_questions.each():
            if parabola.val(["ellipse_question"]) == gathered_random_question:
                answerScore = (ellipse.val()["answerScore"])
                answerId = (ellipse.val()["answerId"])
                solutionScore = (ellipse.val()["solutionScore"])
                solutionId = (ellipse.val()["solutionId"])

        for hyperbola in hyperbola_questions.each():
            if hyperbola.val(["hyperbola _question"]) == gathered_random_question:
                answerScore = (hyperbola.val()["answerScore"])
                answerId = (hyperbola.val()["answerId"])
                solutionScore = (hyperbola.val()["solutionScore"])
                solutionId = (hyperbola.val()["solutionId"])

        return answerScore, answerId, solutionScore, solutionId
    
    def get_scores_for_unit2(gathered_random_question):
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(circle)
        substitution_questions = db.child("precal_questions").child("lesson2").child("substitutionQuestion").get()
        elimination_questions = db.child("precal_questions").child("lesson2").child("eliminationQuestion").get()

        for subs in substitution_questions.each():
            if subs.val(["substitution_question"]) == gathered_random_question:
                answerScore = (subs.val()["answerScore"])
                answerId = (subs.val()["answerId"])
                solutionScore = (subs.val()["solutionScore"])
                solutionId = (subs.val()["solutionId"])

        for elim in elimination_questions.each():
            if elim.val(["elimination_question"]) == gathered_random_question:
                answerScore = (elim.val()["answerScore"])
                answerId = (elim.val()["answerId"])
                solutionScore = (elim.val()["solutionScore"])
                solutionId = (elim.val()["solutionId"])

        return answerScore, answerId, solutionScore, solutionId
    
    def to_json(list_of_ans):
        x={}
        x["intents"] = list_of_ans
        json_object = json.dumps(x, indent = 3)
        with open("1sample.json", "w") as outfile:
            outfile.write(json_object)
    def pre_assess_circle():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(circle)
        circle_questions = db.child("precal_questions").child("pre-assess").child("circleQuestion").get()
        randomize_list = []
        randomize_display_question = []
        question_list = []
        all_solution_dict =[]
        all_answer_dict=[]
        # store all circle_questions key on the circle variable
        for circle in circle_questions.each():
            randomize_list.append(circle.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 1))        
        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            for circle in circle_questions.each():
                if circle.key() == question_key:
                    circle_solutionId = (circle.val()["solutionId"])
                    circle_answerId = (circle.val()["answerId"])
                    circle_question = (circle.val()["circle_1_question"])
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = circle_answerId

                    if circle.val()["answer_num"]=="1":
                        circle_answer1 = (circle.val()["circle_1_answer1"])  
                        answer_dict["patterns"] = [circle_answer1]
                        answer_dict["responses"] = ["correct"]

                    if circle.val()["answer_num"]=="2":
                        circle_answer1 = (circle.val()["circle_1_answer1"])
                        circle_answer2 = (circle.val()["circle_1_answer2"])
                        answer_dict["patterns"] = [circle_answer1,circle_answer2]
                        answer_dict["responses"] = ["correct"]

                    if circle.val()["sol_num"]=="1":
                        circle_solution1 = (circle.val()["circle_1_solution1"])
                        solution_dict["tag"] = circle_solutionId
                        solution_dict["patterns"] = [circle_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if circle.val()["sol_num"]=="2":
                        circle_solution1 = (circle.val()["circle_1_solution1"])
                        circle_solution2 = (circle.val()["circle_1_solution2"])
                        solution_dict["tag"] = circle_solutionId
                        solution_dict["patterns"] = [circle_solution1,circle_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(circle_question)
                    question_list.append(circle_solutionId)
                    question_list.append(circle_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list

        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(parabola)
    def pre_assess_parabola():
        parabola_questions = db.child("precal_questions").child("pre-assess").child("parabolaQuestion").get()
        randomize_list = []
        randomize_display_question = []
        question_list = []
        all_solution_dict=[]
        all_answer_dict=[]
        # store all circle_questions key on the circle variable
        for parabola in parabola_questions.each():
            randomize_list.append(parabola.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 1))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            for parabola in parabola_questions.each():
                if parabola.key() == question_key:
                    parabola_solutionId = (parabola.val()["solutionId"])
                    parabola_answerId = (parabola.val()["answerId"])
                    parabola_question = (parabola.val()["parabola_question"])                    
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = parabola_answerId

                    if parabola.val()["answer_num"]=="1":
                        parabola_answer1 = (parabola.val()["parabola_1_answer1"])  
                        answer_dict["patterns"] = [parabola_answer1]
                        answer_dict["responses"] = ["correct"]

                    if parabola.val()["answer_num"]=="2":
                        parabola_answer1 = (parabola.val()["parabola_answer1"])
                        parabola_answer2 = (parabola.val()["parabola_answer2"])
                        answer_dict["patterns"] = [parabola_answer1,parabola_answer2]
                        answer_dict["responses"] = ["correct"]

                    if parabola.val()["sol_num"]=="1":
                        parabola_solution1 = (parabola.val()["parabola_solution1"])
                        solution_dict["tag"] = parabola_solutionId
                        solution_dict["patterns"] = [parabola_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if parabola.val()["sol_num"]=="2":
                        parabola_solution1 = (parabola.val()["parabola_solution1"])
                        parabola_solution2 = (parabola.val()["parabola_solution2"])
                        solution_dict["tag"] = parabola_solutionId
                        solution_dict["patterns"] = [parabola_solution1,parabola_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(parabola_question)
                    question_list.append(parabola_solutionId)
                    question_list.append(parabola_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list
    def pre_assess_ellipse():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(ellipse)
        ellipse_questions = db.child("precal_questions").child("pre-assess").child("ellipseQuestion").get()
        randomize_display_question = []
        randomize_list = []
        question_list =[]
        all_solution_dict=[]
        all_answer_dict=[]

        # store all circle_questions key on the circle variable
        for ellipse in ellipse_questions.each():
            randomize_list.append(ellipse.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 1))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]
            for ellipse in ellipse_questions.each():

                if ellipse.key() == question_key:
                    ellipse_solutionId = (ellipse.val()["solutionId"])
                    ellipse_answerId = (ellipse.val()["answerId"])
                    ellipse_question = (ellipse.val()["ellipse_question"])
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = ellipse_answerId

                    if ellipse.val()["answer_num"]=="1":
                        ellipse_answer1 = (ellipse.val()["ellipse_answer1"])  
                        answer_dict["patterns"] = [ellipse_answer1]
                        answer_dict["responses"] = ["correct"]

                    if ellipse.val()["answer_num"]=="2":
                        ellipse_answer1 = (ellipse.val()["ellipse_answer1"])
                        ellipse_answer2 = (ellipse.val()["ellipse_answer2"])
                        answer_dict["patterns"] = [ellipse_answer1,ellipse_answer2]
                        answer_dict["responses"] = ["correct"]

                    if ellipse.val()["sol_num"]=="1":
                        ellipse_solution1 = (ellipse.val()["ellipse_solution1"])
                        solution_dict["tag"] = ellipse_solutionId
                        solution_dict["patterns"] = [ellipse_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if ellipse.val()["sol_num"]=="2":
                        ellipse_solution1 = (ellipse.val()["ellipse_solution1"])
                        ellipse_solution2 = (ellipse.val()["ellipse_solution2"])
                        solution_dict["tag"] = ellipse_solutionId
                        solution_dict["patterns"] = [ellipse_solution1,ellipse_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(ellipse_question)
                    question_list.append(ellipse_solutionId)
                    question_list.append(ellipse_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list
    def pre_assess_hyper():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(hyperbola)
        hyperbola_questions = db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").get()
        randomize_list = []
        randomize_display_question = []
        question_list = []
        all_solution_dict =[]
        all_answer_dict=[]
        # store all circle_questions key on the circle variable
        for hyperbola in hyperbola_questions.each():
            randomize_list.append(hyperbola.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 1))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            # DISPLAY QUESTION TO THE WINDOW

            for hyperbola in hyperbola_questions.each():
                if hyperbola.key() == question_key:
                    hyperbola_solutionId = (hyperbola.val()["solutionId"])
                    hyperbola_answerId = (hyperbola.val()["answerId"])
                    hyperbola_question = (hyperbola.val()["hyperbola_question"])
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = hyperbola_answerId

                    if hyperbola.val()["answer_num"]=="1":
                        hyperbola_answer1 = (hyperbola.val()["hyperbola_answer1"])  
                        answer_dict["patterns"] = [hyperbola_answer1]
                        answer_dict["responses"] = ["correct"]

                    if hyperbola.val()["answer_num"]=="2":
                        hyperbola_answer1 = (hyperbola.val()["hyperbola_answer1"])
                        hyperbola_answer2 = (hyperbola.val()["hyperbola_answer2"])
                        answer_dict["patterns"] = [hyperbola_answer1,hyperbola_answer2]
                        answer_dict["responses"] = ["correct"]

                    if hyperbola.val()["sol_num"]=="1":
                        hyperbola_solution1 = (hyperbola.val()["hyperbola_solution1"])
                        solution_dict["tag"] = hyperbola_solutionId
                        solution_dict["patterns"] = [hyperbola_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if hyperbola.val()["sol_num"]=="2":
                        hyperbola_solution1 = (hyperbola.val()["hyperbola_solution1"])
                        hyperbola_solution2 = (hyperbola.val()["hyperbola_solution2"])
                        solution_dict["tag"] = hyperbola_solutionId
                        solution_dict["patterns"] = [hyperbola_solution1,hyperbola_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(hyperbola_question)
                    question_list.append(hyperbola_solutionId)
                    question_list.append(hyperbola_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list
    def pre_assess_elim():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(hyperbola)
        elimination_questions = db.child("precal_questions").child("pre-assess").child("eliminationQuestion").get()
         
        randomize_display_question = []
        randomize_list = []
        question_list = []
        all_solution_dict=[]
        all_answer_dict=[]
        # store all circle_questions key on the circle variable
        for elimination in elimination_questions.each():
            randomize_list.append(elimination.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 1))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            # DISPLAY QUESTION TO THE WINDOW

            for elimination in elimination_questions.each():
                if elimination.key() == question_key:
                    elimination_solutionId = (elimination.val()["solutionId"])
                    elimination_answerId = (elimination.val()["answerId"])
                    elimination_question = (elimination.val()["elimination_question"])
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = elimination_answerId

                    if elimination.val()["answer_num"]=="1":
                        elimination_answer1 = (elimination.val()["elimination_answer1"])  
                        answer_dict["patterns"] = [elimination_answer1]
                        answer_dict["responses"] = ["correct"]

                    if elimination.val()["answer_num"]=="2":
                        elimination_answer1 = (elimination.val()["elimination_answer1"])
                        elimination_answer2 = (elimination.val()["elimination_answer2"])
                        answer_dict["patterns"] = [elimination_answer1,elimination_answer2]
                        answer_dict["responses"] = ["correct"]

                    if elimination.val()["sol_num"]=="1":
                        elimination_solution1 = (elimination.val()["elimination_solution1"])
                        solution_dict["tag"] = elimination_solutionId
                        solution_dict["patterns"] = [elimination_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if elimination.val()["sol_num"]=="2":
                        elimination_solution1 = (elimination.val()["elimination_solution1"])
                        elimination_solution2 = (elimination.val()["elimination_solution2"])
                        solution_dict["tag"] = elimination_solutionId
                        solution_dict["patterns"] = [elimination_solution1,elimination_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(elimination_question)
                    question_list.append(elimination_solutionId)
                    question_list.append(elimination_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list
    def pre_assess_subs():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(hyperbola)
        substitution_questions = db.child("precal_questions").child("pre-assess").child("substitutionQuestion").get()
         
        randomize_display_question = []
        randomize_list = []
        question_list = []
        all_solution_dict=[]
        all_answer_dict=[]
        # store all circle_questions key on the circle variable
        for substitution in substitution_questions.each():
            randomize_list.append(substitution.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 1))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            for substitution in substitution_questions.each():
                if substitution.key() == question_key:
                    substitution_solutionId = (substitution.val()["solutionId"])
                    substitution_answerId = (substitution.val()["answerId"])
                    substitution_question = (substitution.val()["substitution_question"])
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = substitution_answerId

                    if substitution.val()["answer_num"]=="1":
                        substitution_answer1 = (substitution.val()["substitution_answer1"])  
                        answer_dict["patterns"] = [substitution_answer1]
                        answer_dict["responses"] = ["correct"]

                    if substitution.val()["answer_num"]=="2":
                        substitution_answer1 = (substitution.val()["substitution_answer1"])
                        substitution_answer2 = (substitution.val()["substitution_answer2"])
                        answer_dict["patterns"] = [substitution_answer1,substitution_answer2]
                        answer_dict["responses"] = ["correct"]

                    if substitution.val()["sol_num"]=="1":
                        substitution_solution1 = (substitution.val()["substitution_solution1"])
                        solution_dict["tag"] = substitution_solutionId
                        solution_dict["patterns"] = [substitution_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if substitution.val()["sol_num"]=="2":
                        substitution_solution1 = (substitution.val()["substitution_solution1"])
                        substitution_solution2 = (substitution.val()["substitution_solution2"])
                        solution_dict["tag"] = substitution_solutionId
                        solution_dict["patterns"] = [substitution_solution1,substitution_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(substitution_question)
                    question_list.append(substitution_solutionId)
                    question_list.append(substitution_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list
    
    def post_assess_circle():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(circle)
        circle_questions = db.child("precal_questions").child("post-assess").child("circleQuestion").get()
        
        randomize_list = []
        randomize_display_question = []
        question_list =[]
        all_solution_dict=[]
        all_answer_dict=[]
        # store all circle_questions key on the circle variable
        for circle in circle_questions.each():
            randomize_list.append(circle.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 1))
        
        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            for circle in circle_questions.each():
                if circle.key() == question_key:
                    circle_solutionId = (circle.val()["solutionId"])
                    circle_answerId = (circle.val()["answerId"])
                    circle_question = (circle.val()["circle_1_question"])
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = circle_answerId

                    if circle.val()["answer_num"]=="1":
                        circle_answer1 = (circle.val()["circle_1_answer1"])  
                        answer_dict["patterns"] = [circle_answer1]
                        answer_dict["responses"] = ["correct"]

                    if circle.val()["answer_num"]=="2":
                        circle_answer1 = (circle.val()["circle_1_answer1"])
                        circle_answer2 = (circle.val()["circle_1_answer2"])
                        answer_dict["patterns"] = [circle_answer1,circle_answer2]
                        answer_dict["responses"] = ["correct"]

                    if circle.val()["sol_num"]=="1":
                        circle_solution1 = (circle.val()["circle_1_solution1"])
                        solution_dict["tag"] = circle_solutionId
                        solution_dict["patterns"] = [circle_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if circle.val()["sol_num"]=="2":
                        circle_solution1 = (circle.val()["circle_1_solution1"])
                        circle_solution2 = (circle.val()["circle_1_solution2"])
                        solution_dict["tag"] = circle_solutionId
                        solution_dict["patterns"] = [circle_solution1,circle_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(circle_question)
                    question_list.append(circle_solutionId)
                    question_list.append(circle_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list

        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(parabola)
    def post_assess_parabola():
        parabola_questions = db.child("precal_questions").child("post-assess").child("parabolaQuestion").get()
        
        randomize_list = []
        randomize_display_question = []
        question_list = []
        all_solution_dict=[]
        all_answer_dict=[]
        # store all circle_questions key on the circle variable
        for parabola in parabola_questions.each():
            randomize_list.append(parabola.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 1))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            for parabola in parabola_questions.each():
                if parabola.key() == question_key:
                    parabola_solutionId = (parabola.val()["solutionId"])
                    parabola_answerId = (parabola.val()["answerId"])
                    parabola_question = (parabola.val()["parabola_question"])
                    
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = parabola_answerId

                    if parabola.val()["answer_num"]=="1":
                        parabola_answer1 = (parabola.val()["parabola_answer1"])  
                        answer_dict["patterns"] = [parabola_answer1]
                        answer_dict["responses"] = ["correct"]

                    if parabola.val()["answer_num"]=="2":
                        parabola_answer1 = (parabola.val()["parabola_answer1"])
                        parabola_answer2 = (parabola.val()["parabola_answer2"])
                        answer_dict["patterns"] = [parabola_answer1,parabola_answer2]
                        answer_dict["responses"] = ["correct"]

                    if parabola.val()["sol_num"]=="1":
                        parabola_solution1 = (parabola.val()["parabola_solution1"])
                        solution_dict["tag"] = parabola_solutionId
                        solution_dict["patterns"] = [parabola_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if parabola.val()["sol_num"]=="2":
                        parabola_solution1 = (parabola.val()["parabola_solution1"])
                        parabola_solution2 = (parabola.val()["parabola_solution2"])
                        solution_dict["tag"] = parabola_solutionId
                        solution_dict["patterns"] = [parabola_solution1,parabola_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(parabola_question)
                    question_list.append(parabola_solutionId)
                    question_list.append(parabola_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list

    def post_assess_ellipse():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(ellipse)
        ellipse_questions = db.child("precal_questions").child("post-assess").child("ellipseQuestion").get()
        randomize_display_question = []        
        randomize_list = []
        question_list = []
        all_solution_dict=[]
        all_answer_dict=[]
        # store all circle_questions key on the circle variable
        for ellipse in ellipse_questions.each():
            randomize_list.append(ellipse.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 1))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            for ellipse in ellipse_questions.each():

                if ellipse.key() == question_key:
                    ellipse_solutionId = (ellipse.val()["solutionId"])
                    ellipse_answerId = (ellipse.val()["answerId"])
                    ellipse_question = (ellipse.val()["ellipse_question"])
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = ellipse_answerId

                    if ellipse.val()["answer_num"]=="1":
                        ellipse_answer1 = (ellipse.val()["ellipse_answer1"])  
                        answer_dict["patterns"] = [ellipse_answer1]
                        answer_dict["responses"] = ["correct"]

                    if ellipse.val()["answer_num"]=="2":
                        ellipse_answer1 = (ellipse.val()["ellipse_answer1"])
                        ellipse_answer2 = (ellipse.val()["ellipse_answer2"])
                        answer_dict["patterns"] = [ellipse_answer1,ellipse_answer2]
                        answer_dict["responses"] = ["correct"]

                    if ellipse.val()["sol_num"]=="1":
                        ellipse_solution1 = (ellipse.val()["ellipse_solution1"])
                        solution_dict["tag"] = ellipse_solutionId
                        solution_dict["patterns"] = [ellipse_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if ellipse.val()["sol_num"]=="2":
                        ellipse_solution1 = (ellipse.val()["ellipse_solution1"])
                        ellipse_solution2 = (ellipse.val()["ellipse_solution2"])
                        solution_dict["tag"] = ellipse_solutionId
                        solution_dict["patterns"] = [ellipse_solution1,ellipse_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(ellipse_question)
                    question_list.append(ellipse_solutionId)
                    question_list.append(ellipse_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list
    def post_assess_hyper():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(hyperbola)
        hyperbola_questions = db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").get()
        randomize_list = []
        randomize_display_question = []
        question_list = []
        all_solution_dict =[]
        all_answer_dict=[]
        # store all circle_questions key on the circle variable
        for hyperbola in hyperbola_questions.each():
            randomize_list.append(hyperbola.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 1))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            # DISPLAY QUESTION TO THE WINDOW
            for hyperbola in hyperbola_questions.each():
                if hyperbola.key() == question_key:
                    hyperbola_solutionId = (hyperbola.val()["solutionId"])
                    hyperbola_answerId = (hyperbola.val()["answerId"])
                    hyperbola_question = (hyperbola.val()["hyperbola_question"])
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = hyperbola_answerId

                    if hyperbola.val()["answer_num"]=="1":
                        hyperbola_answer1 = (hyperbola.val()["hyperbola_answer1"])  
                        answer_dict["patterns"] = [hyperbola_answer1]
                        answer_dict["responses"] = ["correct"]

                    if hyperbola.val()["answer_num"]=="2":
                        hyperbola_answer1 = (hyperbola.val()["hyperbola_answer1"])
                        hyperbola_answer2 = (hyperbola.val()["hyperbola_answer2"])
                        answer_dict["patterns"] = [hyperbola_answer1,hyperbola_answer2]
                        answer_dict["responses"] = ["correct"]

                    if hyperbola.val()["sol_num"]=="1":
                        hyperbola_solution1 = (hyperbola.val()["hyperbola_solution1"])
                        solution_dict["tag"] = hyperbola_solutionId
                        solution_dict["patterns"] = [hyperbola_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if hyperbola.val()["sol_num"]=="2":
                        hyperbola_solution1 = (hyperbola.val()["hyperbola_solution1"])
                        hyperbola_solution2 = (hyperbola.val()["hyperbola_solution2"])
                        solution_dict["tag"] = hyperbola_solutionId
                        solution_dict["patterns"] = [hyperbola_solution1,hyperbola_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(hyperbola_question)
                    question_list.append(hyperbola_solutionId)
                    question_list.append(hyperbola_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list
    def post_assess_elim():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(hyperbola)
        elimination_questions = db.child("precal_questions").child("post-assess").child("eliminationQuestion").get()
        randomize_display_question = []
        randomize_list = []
        question_list = []
        all_solution_dict=[]
        all_answer_dict=[]
        # store all circle_questions key on the circle variable
        for elimination in elimination_questions.each():
            randomize_list.append(elimination.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 1))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            # DISPLAY QUESTION TO THE WINDOW

            for elimination in elimination_questions.each():
                if elimination.key() == question_key:
                    elimination_solutionId = (elimination.val()["solutionId"])
                    elimination_answerId = (elimination.val()["answerId"])
                    elimination_question = (elimination.val()["elimination_question"])
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = elimination_answerId

                    if elimination.val()["answer_num"]=="1":
                        elimination_answer1 = (elimination.val()["elimination_answer1"])  
                        answer_dict["patterns"] = [elimination_answer1]
                        answer_dict["responses"] = ["correct"]

                    if elimination.val()["answer_num"]=="2":
                        elimination_answer1 = (elimination.val()["elimination_answer1"])
                        elimination_answer2 = (elimination.val()["elimination_answer2"])
                        answer_dict["patterns"] = [elimination_answer1,elimination_answer2]
                        answer_dict["responses"] = ["correct"]

                    if elimination.val()["sol_num"]=="1":
                        elimination_solution1 = (elimination.val()["elimination_solution1"])
                        solution_dict["tag"] = elimination_solutionId
                        solution_dict["patterns"] = [elimination_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if elimination.val()["sol_num"]=="2":
                        elimination_solution1 = (elimination.val()["elimination_solution1"])
                        elimination_solution2 = (elimination.val()["elimination_solution2"])
                        solution_dict["tag"] = elimination_solutionId
                        solution_dict["patterns"] = [elimination_solution1,elimination_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(elimination_question)
                    question_list.append(elimination_solutionId)
                    question_list.append(elimination_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list
    def post_assess_subs():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(hyperbola)
        substitution_questions = db.child("precal_questions").child("post-assess").child("substitutionQuestion").get()  
        randomize_display_question = []
        randomize_list = []
        question_list = []
        all_solution_dict =[]
        all_answer_dict=[]
        # store all circle_questions key on the circle variable
        for substitution in substitution_questions.each():
            randomize_list.append(substitution.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 1))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            for substitution in substitution_questions.each():
                if substitution.key() == question_key:
                    substitution_solutionId = (substitution.val()["solutionId"])
                    substitution_answerId = (substitution.val()["answerId"])
                    substitution_question = (substitution.val()["substitution_question"])
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = substitution_answerId

                    if substitution.val()["answer_num"]=="1":
                        substitution_answer1 = (substitution.val()["substitution_answer1"])  
                        answer_dict["patterns"] = [substitution_answer1]
                        answer_dict["responses"] = ["correct"]

                    if substitution.val()["answer_num"]=="2":
                        substitution_answer1 = (substitution.val()["substitution_answer1"])
                        substitution_answer2 = (substitution.val()["substitution_answer2"])
                        answer_dict["patterns"] = [substitution_answer1,substitution_answer2]
                        answer_dict["responses"] = ["correct"]

                    if substitution.val()["sol_num"]=="1":
                        substitution_solution1 = (substitution.val()["substitution_solution1"])
                        solution_dict["tag"] = substitution_solutionId
                        solution_dict["patterns"] = [substitution_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if substitution.val()["sol_num"]=="2":
                        substitution_solution1 = (substitution.val()["substitution_solution1"])
                        substitution_solution2 = (substitution.val()["substitution_solution2"])
                        solution_dict["tag"] = substitution_solutionId
                        solution_dict["patterns"] = [substitution_solution1,substitution_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(substitution_question)
                    question_list.append(substitution_solutionId)
                    question_list.append(substitution_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list
    def unit_test_elim():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(hyperbola)
        elimination_questions = db.child("precal_questions").child("lesson2").child("eliminationQuestion").get()  
        randomize_display_question = []
        randomize_list = []
        question_list = []
        all_solution_dict = []
        all_answer_dict=[]
        # store all circle_questions key on the circle variable
        for elimination in elimination_questions.each():
            randomize_list.append(elimination.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 5))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            # DISPLAY QUESTION TO THE WINDOW

            for elimination in elimination_questions.each():
                if elimination.key() == question_key:
                    elimination_solutionId = (elimination.val()["solutionId"])
                    elimination_answerId = (elimination.val()["answerId"])
                    elimination_question = (elimination.val()["elimination_question"])
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = elimination_answerId

                    if elimination.val()["answer_num"]=="1":
                        elimination_answer1 = (elimination.val()["elimination_answer1"])  
                        answer_dict["patterns"] = [elimination_answer1]
                        answer_dict["responses"] = ["correct"]

                    if elimination.val()["answer_num"]=="2":
                        elimination_answer1 = (elimination.val()["elimination_answer1"])
                        elimination_answer2 = (elimination.val()["elimination_answer2"])
                        answer_dict["patterns"] = [elimination_answer1,elimination_answer2]
                        answer_dict["responses"] = ["correct"]

                    if elimination.val()["sol_num"]=="1":
                        elimination_solution1 = (elimination.val()["elimination_solution1"])
                        solution_dict["tag"] = elimination_solutionId
                        solution_dict["patterns"] = [elimination_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if elimination.val()["sol_num"]=="2":
                        elimination_solution1 = (elimination.val()["elimination_solution1"])
                        elimination_solution2 = (elimination.val()["elimination_solution2"])
                        solution_dict["tag"] = elimination_solutionId
                        solution_dict["patterns"] = [elimination_solution1,elimination_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(elimination_question)
                    question_list.append(elimination_solutionId)
                    question_list.append(elimination_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list
    def unit_test_subs():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(hyperbola)
        substitution_questions = db.child("precal_questions").child("lesson2").child("substitutionQuestion").get()    
        randomize_display_question = []
        randomize_list = []
        question_list = []
        all_solution_dict =[]
        all_answer_dict =[]
        # store all circle_questions key on the circle variable
        for substitution in substitution_questions.each():
            randomize_list.append(substitution.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 5))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            for substitution in substitution_questions.each():
                if substitution.key() == question_key:
                    substitution_solutionId = (substitution.val()["solutionId"])
                    substitution_answerId = (substitution.val()["answerId"])
                    substitution_question = (substitution.val()["substitution_question"])
                
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = substitution_answerId

                    if substitution.val()["answer_num"]=="1":
                        substitution_answer1 = (substitution.val()["substitution_answer1"])  
                        answer_dict["patterns"] = [substitution_answer1]
                        answer_dict["responses"] = ["correct"]

                    if substitution.val()["answer_num"]=="2":
                        substitution_answer1 = (substitution.val()["substitution_answer1"])
                        substitution_answer2 = (substitution.val()["substitution_answer2"])
                        answer_dict["patterns"] = [substitution_answer1,substitution_answer2]
                        answer_dict["responses"] = ["correct"]

                    if substitution.val()["sol_num"]=="1":
                        substitution_solution1 = (substitution.val()["substitution_solution1"])
                        solution_dict["tag"] = substitution_solutionId
                        solution_dict["patterns"] = [substitution_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if substitution.val()["sol_num"]=="2":
                        substitution_solution1 = (substitution.val()["substitution_solution1"])
                        substitution_solution2 = (substitution.val()["substitution_solution2"])
                        solution_dict["tag"] = substitution_solutionId
                        solution_dict["patterns"] = [substitution_solution1,substitution_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(substitution_question)
                    question_list.append(substitution_solutionId)
                    question_list.append(substitution_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list
    def unit_test_circle():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(circle)
        circle_questions = db.child("precal_questions").child("lesson1").child("circleQuestion").get()        
        randomize_list = []
        randomize_display_question = []
        question_list = []
        all_solution_dict =[]
        all_answer_dict = []

        # store all circle_questions key on the circle variable
        for circle in circle_questions.each():
            randomize_list.append(circle.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 3))
        
        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            for circle in circle_questions.each():
                if circle.key() == question_key:
                    circle_solutionId = (circle.val()["solutionId"])
                    circle_answerId = (circle.val()["answerId"])
                    circle_question = (circle.val()["circle_1_question"])

                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = circle_answerId

                    if circle.val()["answer_num"]=="1":
                        circle_answer1 = (circle.val()["circle_1_answer1"])  
                        answer_dict["patterns"] = [circle_answer1]
                        answer_dict["responses"] = ["correct"]

                    if circle.val()["answer_num"]=="2":
                        circle_answer1 = (circle.val()["circle_1_answer1"])
                        circle_answer2 = (circle.val()["circle_1_answer2"])
                        answer_dict["patterns"] = [circle_answer1,circle_answer2]
                        answer_dict["responses"] = ["correct"]

                    if circle.val()["sol_num"]=="1":
                        circle_solution1 = (circle.val()["circle_1_solution1"])
                        solution_dict["tag"] = circle_solutionId
                        solution_dict["patterns"] = [circle_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if circle.val()["sol_num"]=="2":
                        circle_solution1 = (circle.val()["circle_1_solution1"])
                        circle_solution2 = (circle.val()["circle_1_solution2"])
                        solution_dict["tag"] = circle_solutionId
                        solution_dict["patterns"] = [circle_solution1,circle_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(circle_question)
                    question_list.append(circle_solutionId)
                    question_list.append(circle_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list

        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(parabola)
    def unit_test_parabola():
        parabola_questions = db.child("precal_questions").child("lesson1").child("parabolaQuestion").get()
        randomize_list = []
        randomize_display_question = []
        question_list = []
        all_solution_dict =[]
        all_answer_dict = []

        # store all circle_questions key on the circle variable
        for parabola in parabola_questions.each():
            randomize_list.append(parabola.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 3))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            for parabola in parabola_questions.each():
                if parabola.key() == question_key:
                    parabola_solutionId = (parabola.val()["solutionId"])
                    parabola_answerId = (parabola.val()["answerId"])
                    parabola_question = (parabola.val()["parabola_question"])
                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = parabola_answerId

                    if parabola.val()["answer_num"]=="1":
                        parabola_answer1 = (parabola.val()["parabola_answer1"])  
                        answer_dict["patterns"] = [parabola_answer1]
                        answer_dict["responses"] = ["correct"]

                    if parabola.val()["answer_num"]=="2":
                        parabola_answer1 = (parabola.val()["parabola_answer1"])
                        parabola_answer2 = (parabola.val()["parabola_answer2"])
                        answer_dict["patterns"] = [parabola_answer1,parabola_answer2]
                        answer_dict["responses"] = ["correct"]

                    if parabola.val()["sol_num"]=="1":
                        parabola_solution1 = (parabola.val()["parabola_solution1"])
                        solution_dict["tag"] = parabola_solutionId
                        solution_dict["patterns"] = [parabola_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if parabola.val()["sol_num"]=="2":
                        parabola_solution1 = (parabola.val()["parabola_solution1"])
                        parabola_solution2 = (parabola.val()["parabola_solution2"])
                        solution_dict["tag"] = parabola_solutionId
                        solution_dict["patterns"] = [parabola_solution1,parabola_solution2]
                        solution_dict["responses"] = ["correct"]
                    question_list.append(parabola_question)
                    question_list.append(parabola_solutionId)
                    question_list.append(parabola_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list
    def unit_test_ellipse():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(ellipse)
        ellipse_questions = db.child("precal_questions").child("lesson1").child("ellipseQuestion").get()
        randomize_display_question = []        
        randomize_list = []
        question_list = []
        all_solution_dict = []
        all_answer_dict = []

        # store all circle_questions key on the circle variable
        for ellipse in ellipse_questions.each():
            randomize_list.append(ellipse.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 3))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            for ellipse in ellipse_questions.each():

                if ellipse.key() == question_key:
                    ellipse_solutionId = (ellipse.val()["solutionId"])
                    ellipse_answerId = (ellipse.val()["answerId"])
                    ellipse_question = (ellipse.val()["ellipse_question"])

                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = ellipse_answerId

                    if ellipse.val()["answer_num"]=="1":
                        ellipse_answer1 = (ellipse.val()["ellipse_answer1"])  
                        answer_dict["patterns"] = [ellipse_answer1]
                        answer_dict["responses"] = ["correct"]

                    if ellipse.val()["answer_num"]=="2":
                        ellipse_answer1 = (ellipse.val()["ellipse_answer1"])
                        ellipse_answer2 = (ellipse.val()["ellipse_answer2"])
                        answer_dict["patterns"] = [ellipse_answer1,ellipse_answer2]
                        answer_dict["responses"] = ["correct"]

                    if ellipse.val()["sol_num"]=="1":
                        ellipse_solution1 = (ellipse.val()["ellipse_solution1"])
                        solution_dict["tag"] = ellipse_solutionId
                        solution_dict["patterns"] = [ellipse_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if ellipse.val()["sol_num"]=="2":
                        ellipse_solution1 = (ellipse.val()["ellipse_solution1"])
                        ellipse_solution2 = (ellipse.val()["ellipse_solution2"])
                        solution_dict["tag"] = ellipse_solutionId
                        solution_dict["patterns"] = [ellipse_solution1,ellipse_solution2]
                        solution_dict["responses"] = ["correct"]

                    question_list.append(ellipse_question)
                    question_list.append(ellipse_solutionId)
                    question_list.append(ellipse_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list
    def unit_test_hyper():
        # FETCH RANDOMIZED QUESTIONS FOR PRE-ASSESSMENT(hyperbola)
        hyperbola_questions = db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").get()
        randomize_list = []
        randomize_display_question = []
        question_list = []
        all_solution_dict = []
        all_answer_dict = []
        # store all circle_questions key on the circle variable
        for hyperbola in hyperbola_questions.each():
            randomize_list.append(hyperbola.key())
        # specify how many will questions will be generated, here we use 1
        sampled = (random.sample(randomize_list, 3))

        # store all the randomized questions to be displayed
        randomize_display_question.append(sampled)

        for questions in range(len(sampled)):
            question_key = sampled[questions]

            # DISPLAY QUESTION TO THE WINDOW

            for hyperbola in hyperbola_questions.each():
                if hyperbola.key() == question_key:
                    hyperbola_solutionId = (hyperbola.val()["solutionId"])
                    hyperbola_answerId = (hyperbola.val()["answerId"])
                    hyperbola_question = (hyperbola.val()["hyperbola_question"])

                    answer_dict = {}
                    solution_dict = {}

                    answer_dict["tag"] = hyperbola_answerId

                    if hyperbola.val()["answer_num"]=="1":
                        hyperbola_answer1 = (hyperbola.val()["hyperbola_answer1"])  
                        answer_dict["patterns"] = [hyperbola_answer1]
                        answer_dict["responses"] = ["correct"]

                    if hyperbola.val()["answer_num"]=="2":
                        hyperbola_answer1 = (hyperbola.val()["hyperbola_answer1"])
                        hyperbola_answer2 = (hyperbola.val()["hyperbola_answer2"])
                        answer_dict["patterns"] = [hyperbola_answer1,hyperbola_answer2]
                        answer_dict["responses"] = ["correct"]

                    if hyperbola.val()["sol_num"]=="1":
                        hyperbola_solution1 = (hyperbola.val()["hyperbola_solution1"])
                        solution_dict["tag"] = hyperbola_solutionId
                        solution_dict["patterns"] = [hyperbola_solution1]
                        solution_dict["responses"] = ["correct"]
                    
                    if hyperbola.val()["sol_num"]=="2":
                        hyperbola_solution1 = (hyperbola.val()["hyperbola_solution1"])
                        hyperbola_solution2 = (hyperbola.val()["hyperbola_solution2"])
                        solution_dict["tag"] = hyperbola_solutionId
                        solution_dict["patterns"] = [hyperbola_solution1,hyperbola_solution2]
                        solution_dict["responses"] = ["correct"]

                    question_list.append(hyperbola_question)
                    question_list.append(hyperbola_solutionId)
                    question_list.append(hyperbola_answerId)
                    all_solution_dict.append(solution_dict)
                    all_answer_dict.append(answer_dict)
        return all_answer_dict, all_solution_dict, question_list
    
# 6 question for unitTest2 elim and subs
# 3 questions for unitTest1 circ,para,ellip,hyper
# 2 questions for pre-Assess circ,para,ellip,hyper,elim and subs
# 2 questions for post-assess circ,para,ellip,hyper,elim and subs



# 28
#  IF USER WILL CREATE THEIR OWN PRE-CAL QUESTIONS

# circle_1_question = "Write the circle equation in standard form. x^2 + y^2 - 6x + 8y + 4 = 0"
# circle_1_answer1 = "(x-3)^2+(y+4)^2=21"
# circle_1_answer2 = "-"
# circle_1_solution1 = "x^2-6x+y^2+8y=-4 x^2-6x+9+y^2+8y+16=-4+9+16 (x-3)^2+(y+4)^2=21"
# circle_1_solution2 = "-"
# questionId = "circle_27_question"
# checkId = "active"
# answerId = "question_27_answer"
# answer_num = "1"
# solutionId = "question_27_solution"
# sol_num = "2"

# data ={"questionId":questionId,"circle_1_question":circle_1_question,
#        "circle_1_solution1": circle_1_solution1,"circle_1_solution2": circle_1_solution2,
#        "circle_1_answer1":circle_1_answer1, "circle_1_answer2":circle_1_answer2, 
#        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, "solutionId":solutionId, 
#        "sol_num":sol_num}
# db.child("precal_questions").child("post-assess").child("circleQuestion").push(data)
# print("completed")

# parabola_question = "Find the center of this ellipse. ((x^2/49) + (y^2/169)) = 1"
# parabola_answer1 = "center(0,0)"
# parabola_answer2 = "0,0"
# parabola_solution1 = "h=0 k=0"
# parabola_solution2 = "(x-h)^2 /a^2 + (y-k)^2/b^2 =1"
# questionId = "question_21"
# checkId = "active"
# answerId = "question_21_answer"
# answer_num = "2"
# solutionId = "question_20_solution"
# sol_num = "2"

# data ={"questionId":questionId,"parabola_question":parabola_question,
#        "parabola_solution1": parabola_solution1,"parabola_solution2": parabola_solution2,"parabola_answer1":parabola_answer1,
#        "parabola_answer2":parabola_answer2, "isActive":checkId, "answerId":answerId,
#        "answer_num":answer_num, "solutionId":solutionId, "sol_num":sol_num}
# db.child("precal_questions").child("pre-assess").child("parabolaQuestion").push(data)
# print("completed")

# ellipse_question = "Find the center of this ellipse. ((x^2/49) + (y^2/169)) = 1"
# ellipse_answer1 = "center(0,0)"
# ellipse_answer2 = "0,0"
# ellipse_solution1 = "h=0 k=0"
# ellipse_solution2 = "(x-h)^2 /a^2 + (y-k)^2/b^2 =1"
# questionId = "question_21"
# checkId = "active"
# answerId = "question_21_answer"
# answer_num = "2"
# solutionId = "question_21_solution"
# sol_num = "2"

# data ={"questionId":questionId,"ellipse_question":ellipse_question,
#        "ellipse_solution1": ellipse_solution1,"ellipse_solution2": ellipse_solution2,"ellipse_answer1":ellipse_answer1,
#        "ellipse_answer2":ellipse_answer2, "isActive":checkId, "answerId":answerId,
#        "answer_num":answer_num, "solutionId":solutionId, "sol_num":sol_num}
# db.child("precal_questions").child("pre-assess").child("ellipseQuestion").push(data)
# print("completed")

# hyperbola_question = "Simplify the hyperbolic equation to standard form. 4x^2 - 5y^2 + 32x + 30y = 1"
# hyperbola_answer1 = "(x+4)^2/5-(y-3)^2/4=1"
# hyperbola_answer2 = "(x+4)^2/5-(y-3)^2/4=1"
# hyperbola_solution1 = "4(x^2+8x)-5(y^2-6y)=1 4(x^2+8x+16)-5(y^2-6y+9)=1+4(16)-5(9) 4(x+4)^2-5(y-3)^2=20 (x+4)^2/5-(y-3)^2/4=1"
# hyperbola_solution2 = "-"
# questionId = "question_26"
# checkId = "active"
# answerId = "question_26_answer"
# answer_num = "2"
# solutionId = "question_26_solution"
# sol_num = "1"

# data ={"questionId":questionId,"hyperbola_question":hyperbola_question,
#        "hyperbola_solution1": hyperbola_solution1,"hyperbola_solution2": hyperbola_solution2,
#        "hyperbola_answer1":hyperbola_answer1, "hyperbola_answer2":hyperbola_answer2,
#        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, 
#        "solutionId":solutionId, "sol_num":sol_num}
# db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").push(data)
# print("completed")

# elimination_question = "Use Elimination method to solve the system. y^2 - 4x - 6y = 11, 4(3-x) = (y-3)^2"
# elimination_answer1 = "(-1,7),(-1,-1)"
# elimination_answer2 = "(-1,7),(-1,-1)"
# elimination_solution1 = "4(3-x)=(y-3)^2 12-4x=y^2-6y+9 y^2+4x-6y=3 y^2-4x-6y=11 y^2-4x-6y=3 2y^2-12y=14 y^2-6y-7=0 (y-7)(y+1)=0 y=7 y=-1 x=3-((y-3)^2/4) y=7 x=-1 y=-1 x=-1"
# elimination_solution2 = "-"
# questionId = "question_29"
# checkId = "active"
# answerId = "question_29_answer"
# answer_num = "2"
# solutionId = "question_29_solution"
# sol_num = "1"

# data ={"questionId":questionId,"elimination_question":elimination_question,
#        "elimination_solution1": elimination_solution1,"elimination_solution2": elimination_solution2,
#        "elimination_answer1":elimination_answer1, "elimination_answer2":elimination_answer2,
#        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, 
#        "solutionId":solutionId, "sol_num":sol_num}
# db.child("precal_questions").child("post-assess").child("eliminationQuestion").push(data)
# print("completed")

# substitution_question = "Find the center and radius of this circle. x^2 + y^2 - 6x = 7"
# substitution_answer1 = "center(3,0) radius=4"
# substitution_answer2 = "center(3,0) r=4"
# substitution_answer3 = "c=(3,0) r=4"
# substitution_answer4 = "(3,0) r=4"
# substitution_solution1 = "x^2+y^2-6x=7 x^2-6x+9+y^2=7+9 (x-3)^2+y^2=16"
# substitution_solution2 = "-"
# questionId = "question_30"
# checkId = "active"
# answerId = "question_30_answer"
# answer_num = "2"
# solutionId = "question_30_solution"
# sol_num = "2"

# data ={"questionId":questionId,"substitution_question":substitution_question,
#        "substitution_solution1": substitution_solution1,"substitution_solution2": substitution_solution2,
#        "substitution_answer1":substitution_answer1,"substitution_answer2":substitution_answer2, 
#        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, 
#        "solutionId":solutionId, "sol_num":sol_num}
# db.child("precal_questions").child("post-assess").child("substitutionQuestion").push(data)
# print("completed")
