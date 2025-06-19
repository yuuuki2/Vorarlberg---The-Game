using CommunityToolkit.Mvvm.ComponentModel;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;

namespace Game
{
    /// @class SuchViewModel
    /// @brief View model for the search functionality
    /// @details This class implements the MVVM pattern for handling search operations
    ///          and manages the stop locations data and filtering functionality
    public partial class SuchViewModel : ObservableObject
    {
        /// @brief Selected stop location
        /// @details Observable property that holds the currently selected stop
        [ObservableProperty]
        private string? selectedStop;

        /// @brief Search text input
        /// @details Observable property that holds the current search text
        [ObservableProperty]
        private string? searchText;

        /// @brief Dictionary of stop locations
        /// @details Contains mapping of stop names to their identifiers
        public Dictionary<string, string> Haltestellen { get; }

        /// @brief Collection of filtered stops
        /// @details Observable collection of stops filtered based on search criteria
        public ObservableCollection<string> FilteredStops { get; }

        /// @brief Constructor for SuchViewModel
        /// @param haltestellen Dictionary containing the stop locations data
        /// @details Initializes the view model with the provided stop locations
        public SuchViewModel(Dictionary<string, string> haltestellen)
        {
            Haltestellen = haltestellen;
            FilteredStops = new ObservableCollection<string>(Haltestellen.Values);
        }

        // Korrektur: Partial Method korrekt implementiert
        partial void OnSearchTextChanged(string? value)
        {
            if (string.IsNullOrWhiteSpace(value))
            {
                FilteredStops.Clear();
                foreach (var stop in Haltestellen.Values)
                    FilteredStops.Add(stop);
            }
            else
            {
                var filtered = Haltestellen.Values
                    .Where(s => s.Contains(value, System.StringComparison.OrdinalIgnoreCase))
                    .ToList();

                FilteredStops.Clear();
                foreach (var stop in filtered)
                    FilteredStops.Add(stop);
            }
        }
    }
}