#include <algorithm>
#include <limits>
#include <memory>
#include <vector>

template<typename ResourcePtr>
class WeightedArbiter
{
    static_assert(std::is_pointer<ResourcePtr>::value, "WeightedArbiter may only be instantiated with pointer types");

public:
    static constexpr uint32_t MaxNumberOfResoures = std::numeric_limits<int>::max(); // Maximum number of Resources

    using WeightType            = uint8_t;
    using AccumulatedWeightType = uint16_t;
    using ResourceType          = std::pair<ResourcePtr, WeightType>;

    // WeightedArbiter(const WeightedArbiter&)             = delete;
    // WeightedArbiter& operator =(const WeightedArbiter&) = delete;

    explicit WeightedArbiter();
    ~WeightedArbiter();

public:
    bool empty() const;

    std::size_t size() const;

    void push(ResourceType resource);

    ResourcePtr pop();

    void clear();

private:
    void initialize();

    void calcAccumulatedWeights();

    void calcSumOfAccumulatedWeights();

    void incSelectionHelpNumber();

private:
    std::vector<ResourceType>          resources_;
    std::vector<AccumulatedWeightType> accumulatedWeights_;      // Accumulated Weights, [weight0 - 1, weight0 + weight1 - 1, ..., weight0 + weight1 +...+ weightn - 1]
    uint32_t                           selectionHelperNumber_;   // Help number, will be set to 0 when reach max value
    uint8_t                            currentIndex_;            // Current index of allocated resources
    AccumulatedWeightType              sumOfAccumulatedWeights_; // Sum of all Accumulated Weight
    bool                               hasInitialized;           // Whether proper initialization has been done or not
};

template<typename ResourcePtr>
WeightedArbiter<ResourcePtr>::WeightedArbiter()
    : selectionHelperNumber_(0),
    currentIndex_(0),
    sumOfAccumulatedWeights_(0),
    hasInitialized(false)
{
}

template<typename ResourcePtr>
WeightedArbiter<ResourcePtr>::~WeightedArbiter()
{
    clear();
}

template<typename ResourcePtr>
inline bool WeightedArbiter<ResourcePtr>::empty() const
{
    return resources_.empty();
}

template<typename ResourcePtr>
inline std::size_t WeightedArbiter<ResourcePtr>::size() const
{
    return resources_.size();
}

template<typename ResourcePtr>
void WeightedArbiter<ResourcePtr>::clear()
{
    for (const auto& resource : resources_)
    {
        delete resource.first;
    }

    resources_.clear();
    hasInitialized = false;
}

template<typename ResourcePtr>
void WeightedArbiter<ResourcePtr>::push(ResourceType resource)
{
    if (resource.first && resource.second > 0)
    {
        resources_.emplace_back(resource);
        hasInitialized = false;
    }
    else
    {
        // print warning message here.
    }
}

template<typename ResourcePtr>
ResourcePtr WeightedArbiter<ResourcePtr>::pop()
{
    if (!hasInitialized)
    {
        initialize();
    }

    uint32_t selectionNumber = selectionHelperNumber_ % sumOfAccumulatedWeights_;

    if (selectionNumber <= accumulatedWeights_[currentIndex_])
    {
        currentIndex_ = (selectionNumber == 0 ? 0 : currentIndex_);
    }
    else
    {
        currentIndex_ = ((currentIndex_ + 1) % resources_.size());
    }

    incSelectionHelpNumber();

    return resources_[currentIndex_];
}

template<typename ResourcePtr>
void WeightedArbiter<ResourcePtr>::initialize()
{
    srand(time(nullptr));

    selectionHelperNumber_ = rand();
    currentIndex_          = 0;

    calcAccumulatedWeights();
    calcSumOfAccumulatedWeights();

    hasInitialized = true;
}

template<typename ResourcePtr>
void WeightedArbiter<ResourcePtr>::calcAccumulatedWeights()
{
    accumulatedWeights_.reserve(resources_.size());

    uint8_t currentWeight = resources_.front().second;
    accumulatedWeights_.emplace_back(currentWeight);

    for (uint8_t i = 1; i < resources_.size(); ++i)
    {
        currentWeight = resources_[i].second;
        accumulatedWeights_.emplace_back(accumulatedWeights_.back() + currentWeight);
    }
}

template<typename ResourcePtr>
void WeightedArbiter<ResourcePtr>::calcSumOfAccumulatedWeights()
{
    sumOfAccumulatedWeights_ = 0;

    for (const auto& accumulatedWeight : accumulatedWeights_)
    {
        sumOfAccumulatedWeights_ += accumulatedWeight;
    }
}

template<typename ResourcePtr>
void WeightedArbiter<ResourcePtr>::incSelectionHelpNumber()
{
    selectionHelperNumber_ = (selectionHelperNumber_ == MaxNumberOfResoures ? 0 : selectionHelperNumber_ + 1);
}
