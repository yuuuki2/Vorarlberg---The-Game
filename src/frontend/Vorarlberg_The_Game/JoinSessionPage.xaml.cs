namespace Game;

/// @class JoinSessionPage
/// @brief Page class for handling session joining functionality
/// @details This class manages the user interface and logic for joining
///          an existing game session
public partial class JoinSessionPage : ContentPage
{
    /// @brief Constructor for the JoinSessionPage
    /// @details Initializes the components of the join session page
    public JoinSessionPage()
    {
        InitializeComponent();
    }

    /// @brief Event handler for the join button click
    /// @param sender The object that triggered the event
    /// @param e The event arguments
    /// @details Validates the session code and attempts to join the session
    private async void OnJoinClicked(object sender, EventArgs e)
    {
        string sessionCode = SessionCodeEntry.Text;

        if (string.IsNullOrWhiteSpace(sessionCode))
        {
            await DisplayAlert("Error", "Please enter a session code.", "OK");
            return;
        }

        var players = new List<string> { "You", "Player 1", "Player 2" };

        await Navigation.PushModalAsync(new NavigationPage(new RoomPage(players)));
    }

    private async void OnBackClicked(object sender, EventArgs e)
    {
        await Navigation.PopModalAsync();
    }
}