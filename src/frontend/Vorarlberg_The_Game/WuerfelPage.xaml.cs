using System;
using Microsoft.Maui.Controls;

namespace Game
{
    /// @class WuerfelPage
    /// @brief Page class for the dice rolling interface
    /// @details This class manages the user interface and interactions
    ///          for the dice rolling feature
    public partial class WuerfelPage : ContentPage
    {
        /// @brief View model instance for the dice rolling functionality
        private readonly WuerfelViewModel _viewModel;

        /// @brief Constructor for WuerfelPage
        /// @param viewModel The view model instance to use
        /// @details Initializes the page components and sets up data binding
        public WuerfelPage(WuerfelViewModel viewModel)
        {
            InitializeComponent();
            _viewModel = viewModel;
            BindingContext = _viewModel;
        }

        /// @brief Event handler for the roll button click
        /// @param sender The object that triggered the event
        /// @param e The event arguments
        /// @details Executes the roll dice command from the view model
        private async void OnRollClicked(object sender, EventArgs e)
        {
            _viewModel.RollDiceCommand.Execute(null);

            await DiceImageView.ScaleTo(0.8, 100);

            DiceImageView.Rotation = 0;

            await DiceImageView.RotateTo(360, 300);
            await DiceImageView.ScaleTo(1.0, 100);
        }



        /// @brief Event handler for the close button click
        /// @param sender The object that triggered the event
        /// @param e The event arguments
        /// @details Closes the modal page and returns to the previous page
        private async void OnCloseClicked(object sender, EventArgs e)
        {
            await Navigation.PopModalAsync();
        }
    }
}
