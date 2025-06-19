using System;
using Microsoft.Maui.Controls;
using Microsoft.Extensions.Logging;

namespace Game
{
    /// @class WuerfelPage
    /// @brief Page class for the dice rolling interface
    /// @details This class manages the user interface and interactions
    ///          for the dice rolling feature
    public partial class WuerfelPage : ContentPage
    {
        private readonly WuerfelViewModel _viewModel;
        private readonly ILogger<WuerfelPage> _logger;

        /// @brief Constructor for WuerfelPage
        /// @param viewModel The view model instance to use
        /// @details Initializes the page components and sets up data binding
        public WuerfelPage(WuerfelViewModel viewModel, ILogger<WuerfelPage> logger)
        {
            _viewModel = viewModel;
            _logger = logger;

            _logger.LogInformation("Initializing WuerfelPage...");
            InitializeComponent();
            BindingContext = _viewModel;
            _logger.LogInformation("WuerfelPage initialized.");
        }

        /// @brief Event handler for the roll button click
        private async void OnRollClicked(object sender, EventArgs e)
        {
            _logger.LogInformation("Roll button clicked – executing dice roll.");
            _viewModel.RollDiceCommand.Execute(null);

            await DiceImageView.ScaleTo(0.8, 100);
            DiceImageView.Rotation = 0;
            await DiceImageView.RotateTo(360, 300);
            await DiceImageView.ScaleTo(1.0, 100);
            _logger.LogInformation("Dice animation completed.");
        }

        /// @brief Event handler for the close button click
        private async void OnCloseClicked(object sender, EventArgs e)
        {
            _logger.LogInformation("Close button clicked – closing WuerfelPage.");
            await Navigation.PopModalAsync();
        }
    }
}
