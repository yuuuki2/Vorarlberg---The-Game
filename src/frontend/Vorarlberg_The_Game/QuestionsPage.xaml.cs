using System.Collections.Generic;
using Microsoft.Maui.Controls;

namespace Game
{
    /// @class QuestionsPage
    /// @brief Page class for managing game questions
    /// @details Handles the display and interaction with available questions,
    ///          current questions, and past questions with answers
    public partial class QuestionsPage : ContentPage
    {
        /// @class QuestionAnswer
        /// @brief Model class for question-answer pairs
        /// @details Represents a single question and its corresponding answer
        public class QuestionAnswer
        {
            /// @brief The question text
            public string Question { get; set; } = string.Empty;
            /// @brief The answer text
            public string Answer { get; set; } = string.Empty;
        }

        /// @brief Constructor for QuestionsPage
        /// @details Initializes the page with example questions and answers
        public QuestionsPage()
        {
            InitializeComponent();

            // Beispiel-Daten
            var availableQuestions = new List<string>
            {
                "Where are you?",
                "How many cards do you have?"
            };

            var pastQA = new List<QuestionAnswer>
            {
                new QuestionAnswer
                {
                    Question = "What's your role?",
                    Answer   = "Hider"
                },
                new QuestionAnswer
                {
                    Question = "Start time?",
                    Answer   = "2025-06-16 14:00"
                }
            };

            AvailableQuestionsView.ItemsSource = availableQuestions;
            CurrentQuestionLabel.Text = "Where are you?";
            PastQAView.ItemsSource = pastQA;
        }

        /// <summary>
        /// Navigiert zur�ck zur LiveMapPage.
        /// </summary>
        private async void OnBackClicked(object sender, System.EventArgs e)
        {
            await Navigation.PopModalAsync();
        }
    }
}
