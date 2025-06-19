using Microsoft.Maui.Controls;

namespace Game
{
    /// @class SuchePage
    /// @brief Page class for the stop search functionality
    /// @details Manages the search interface for transit stops,
    ///          including search functionality and selection handling
    public partial class SuchePage : ContentPage
    {
        /// @brief View model instance for the search functionality
        private readonly SuchViewModel _viewModel;

        /// @brief Task completion source for async selection handling
        private readonly TaskCompletionSource<string?> _tcs;

        /// @brief Constructor for SuchePage
        /// @param haltestellen Dictionary of available stops
        /// @param tcs Task completion source for handling selection
        /// @details Initializes the search page with available stops and binds the view model
        public SuchePage(Dictionary<string, string> haltestellen, TaskCompletionSource<string?> tcs)
        {
            InitializeComponent();
            _tcs = tcs;
            _viewModel = new SuchViewModel(haltestellen);
            BindingContext = _viewModel;
        }

        /// @brief Event handler for the confirm button
        /// @param sender The object that triggered the event
        /// @param e The event arguments
        /// @details Processes the selected stop and completes the selection task
        private async void Confirm_Clicked(object sender, System.EventArgs e)
        {
            if (!string.IsNullOrEmpty(_viewModel.SelectedStop))
            {
                var selectedId = _viewModel.Haltestellen
                    .FirstOrDefault(x => x.Value == _viewModel.SelectedStop).Key;

                _tcs.SetResult(selectedId);
                await Navigation.PopModalAsync();
            }
            else
            {
                await DisplayAlert("Auswahl ben�tigt", "Bitte w�hlen Sie eine Haltestelle aus", "OK");
            }
        }

        /// @brief Event handler for the cancel button
        /// @param sender The object that triggered the event
        /// @param e The event arguments
        /// @details Cancels the selection and closes the search page
        private async void Cancel_Clicked(object sender, System.EventArgs e)
        {
            _tcs.SetResult(null);
            await Navigation.PopModalAsync();
        }
    }
}