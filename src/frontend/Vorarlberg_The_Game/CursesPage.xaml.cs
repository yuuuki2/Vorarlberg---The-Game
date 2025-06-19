using System.Collections.Generic;
using Microsoft.Maui.Controls;

namespace Game
{
    /// @class CursesPage
    /// @brief Page for displaying active curses
    /// @details Shows all currently active curses affecting the Seekers,
    ///          including their effects and duration
    public partial class CursesPage : ContentPage
    {
        /// @brief Constructor for CursesPage
        /// @details Initializes the page with hardcoded example curses
        public CursesPage()
        {
            InitializeComponent();

            // Example curses
            CursesView.ItemsSource = new List<string>
            {
                "Slow",
                "Blind",
                "Confusion"
            };
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
