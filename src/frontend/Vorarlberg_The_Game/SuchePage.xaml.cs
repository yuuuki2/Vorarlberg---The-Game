using Microsoft.Maui.Controls;
using Microsoft.Extensions.Logging;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Game
{
    /// @class SuchePage
    /// @brief Page class for the stop search functionality
    /// @details Manages the search interface for transit stops,
    ///          including search functionality and selection handling
    public partial class SuchePage : ContentPage
    {
        private readonly SuchViewModel _viewModel;
        private readonly TaskCompletionSource<string?> _tcs;
        private readonly ILogger<SuchePage> _logger;

        /// @brief Constructor for SuchePage
        /// @param haltestellen Dictionary of available stops
        /// @param tcs Task completion source for handling selection
        /// @details Initializes the search page with available stops and binds the view model
        public SuchePage(Dictionary<string, string> haltestellen, TaskCompletionSource<string?> tcs, ILogger<SuchePage> logger)
        {
            InitializeComponent();
            _logger = logger;
            _logger.LogInformation("Initializing SuchePage with {Count} stops...", haltestellen?.Count ?? 0);

            _tcs = tcs;
            _viewModel = new SuchViewModel(haltestellen);
            BindingContext = _viewModel;

            _logger.LogInformation("SuchePage initialized.");
        }

        /// @brief Event handler for the confirm button
        private async void Confirm_Clicked(object sender, System.EventArgs e)
        {
            _logger.LogInformation("Confirm button clicked.");

            if (!string.IsNullOrEmpty(_viewModel.SelectedStop))
            {
                var selectedId = _viewModel.Haltestellen
                    .FirstOrDefault(x => x.Value == _viewModel.SelectedStop).Key;

                _logger.LogInformation("Selected stop: {Stop} (ID: {ID})", _viewModel.SelectedStop, selectedId);
                _tcs.SetResult(selectedId);
                await Navigation.PopModalAsync();
            }
            else
            {
                _logger.LogWarning("No stop selected – showing alert.");
                await DisplayAlert("Auswahl benötigt", "Bitte wählen Sie eine Haltestelle aus", "OK");
            }
        }

        /// @brief Event handler for the cancel button
        private async void Cancel_Clicked(object sender, System.EventArgs e)
        {
            _logger.LogInformation("Cancel button clicked – selection canceled.");
            _tcs.SetResult(null);
            await Navigation.PopModalAsync();
        }
    }
}
