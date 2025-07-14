#!/usr/bin/env python3
"""
Pattern Confidence Scoring Engine

This engine calculates and tracks confidence scores for pattern matches,
learning from historical success rates and adapting scores based on
actual usage and outcomes.

Features:
- Dynamic confidence calculation
- Historical performance tracking
- Success rate learning
- Multi-factor confidence assessment
- Adaptive scoring algorithms
"""

import json
import logging
import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from enum import Enum
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfidenceFactor(Enum):
    """Factors that influence confidence scoring"""
    HISTORICAL_SUCCESS = "historical_success"
    PATTERN_COMPLETENESS = "pattern_completeness"
    USAGE_FREQUENCY = "usage_frequency"
    RECENCY = "recency"
    DOMAIN_ALIGNMENT = "domain_alignment"
    COMPLEXITY_MATCH = "complexity_match"
    VALIDATION_COVERAGE = "validation_coverage"
    USER_FEEDBACK = "user_feedback"


@dataclass
class PatternUsage:
    """Track individual pattern usage"""
    pattern_id: str
    timestamp: datetime
    success: bool
    context: Dict
    confidence_at_time: float
    actual_outcome: Optional[str] = None
    feedback_score: Optional[float] = None


@dataclass
class ConfidenceScore:
    """Detailed confidence score with breakdown"""
    overall_score: float
    factor_scores: Dict[ConfidenceFactor, float]
    reliability: float  # How reliable is this confidence score
    sample_size: int
    last_updated: datetime
    trend: str  # 'improving', 'stable', 'declining'
    recommendations: List[str] = field(default_factory=list)


@dataclass
class PatternPerformance:
    """Track pattern performance over time"""
    pattern_id: str
    total_uses: int
    successful_uses: int
    success_rate: float
    average_confidence: float
    confidence_accuracy: float  # How accurate confidence predictions have been
    usage_trend: List[Tuple[datetime, bool]]  # Recent usage history
    last_used: datetime


class ConfidenceScorer:
    """
    Engine for calculating and tracking pattern confidence scores
    based on historical performance and multiple factors
    """
    
    def __init__(self, knowledge_base_path: str, history_path: Optional[str] = None):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.history_path = Path(history_path) if history_path else self.knowledge_base_path / "performance-metrics"
        
        self.pattern_history: Dict[str, List[PatternUsage]] = defaultdict(list)
        self.pattern_performance: Dict[str, PatternPerformance] = {}
        self.confidence_weights = self._initialize_weights()
        self.learning_rate = 0.1
        
        self.load_historical_data()
    
    def _initialize_weights(self) -> Dict[ConfidenceFactor, float]:
        """Initialize factor weights for confidence calculation"""
        return {
            ConfidenceFactor.HISTORICAL_SUCCESS: 0.30,
            ConfidenceFactor.PATTERN_COMPLETENESS: 0.20,
            ConfidenceFactor.USAGE_FREQUENCY: 0.15,
            ConfidenceFactor.RECENCY: 0.10,
            ConfidenceFactor.DOMAIN_ALIGNMENT: 0.10,
            ConfidenceFactor.COMPLEXITY_MATCH: 0.05,
            ConfidenceFactor.VALIDATION_COVERAGE: 0.05,
            ConfidenceFactor.USER_FEEDBACK: 0.05
        }
    
    def load_historical_data(self):
        """Load historical pattern usage data"""
        try:
            # Load pattern usage history
            history_file = self.history_path / "pattern-usage-history.json"
            if history_file.exists():
                with open(history_file, 'r') as f:
                    history_data = json.load(f)
                    
                    for pattern_id, usages in history_data.items():
                        self.pattern_history[pattern_id] = [
                            PatternUsage(
                                pattern_id=usage['pattern_id'],
                                timestamp=datetime.fromisoformat(usage['timestamp']),
                                success=usage['success'],
                                context=usage.get('context', {}),
                                confidence_at_time=usage.get('confidence_at_time', 0.5),
                                actual_outcome=usage.get('actual_outcome'),
                                feedback_score=usage.get('feedback_score')
                            )
                            for usage in usages
                        ]
                
                logger.info(f"Loaded history for {len(self.pattern_history)} patterns")
            
            # Load performance summaries
            performance_file = self.history_path / "pattern-performance.json"
            if performance_file.exists():
                with open(performance_file, 'r') as f:
                    performance_data = json.load(f)
                    
                    for pattern_id, perf in performance_data.items():
                        self.pattern_performance[pattern_id] = PatternPerformance(
                            pattern_id=pattern_id,
                            total_uses=perf['total_uses'],
                            successful_uses=perf['successful_uses'],
                            success_rate=perf['success_rate'],
                            average_confidence=perf['average_confidence'],
                            confidence_accuracy=perf.get('confidence_accuracy', 0.5),
                            usage_trend=[
                                (datetime.fromisoformat(t[0]), t[1])
                                for t in perf.get('usage_trend', [])
                            ],
                            last_used=datetime.fromisoformat(perf['last_used'])
                        )
                
                logger.info(f"Loaded performance data for {len(self.pattern_performance)} patterns")
                
        except Exception as e:
            logger.error(f"Error loading historical data: {e}")
    
    def calculate_confidence(self, pattern_id: str, pattern_data: Dict, 
                           context: Dict) -> ConfidenceScore:
        """
        Calculate comprehensive confidence score for a pattern
        
        Args:
            pattern_id: Unique pattern identifier
            pattern_data: Pattern content and metadata
            context: Current usage context
            
        Returns:
            ConfidenceScore with detailed breakdown
        """
        factor_scores = {}
        recommendations = []
        
        # Calculate each factor score
        factor_scores[ConfidenceFactor.HISTORICAL_SUCCESS] = self._calculate_historical_success(pattern_id)
        factor_scores[ConfidenceFactor.PATTERN_COMPLETENESS] = self._calculate_pattern_completeness(pattern_data)
        factor_scores[ConfidenceFactor.USAGE_FREQUENCY] = self._calculate_usage_frequency(pattern_id)
        factor_scores[ConfidenceFactor.RECENCY] = self._calculate_recency_score(pattern_id)
        factor_scores[ConfidenceFactor.DOMAIN_ALIGNMENT] = self._calculate_domain_alignment(pattern_data, context)
        factor_scores[ConfidenceFactor.COMPLEXITY_MATCH] = self._calculate_complexity_match(pattern_data, context)
        factor_scores[ConfidenceFactor.VALIDATION_COVERAGE] = self._calculate_validation_coverage(pattern_data)
        factor_scores[ConfidenceFactor.USER_FEEDBACK] = self._calculate_user_feedback_score(pattern_id)
        
        # Calculate weighted overall score
        overall_score = sum(
            factor_scores[factor] * self.confidence_weights[factor]
            for factor in ConfidenceFactor
        )
        
        # Calculate reliability of the confidence score
        reliability = self._calculate_reliability(pattern_id, factor_scores)
        
        # Get sample size
        sample_size = len(self.pattern_history.get(pattern_id, []))
        
        # Determine trend
        trend = self._determine_trend(pattern_id)
        
        # Generate recommendations
        if factor_scores[ConfidenceFactor.HISTORICAL_SUCCESS] < 0.5:
            recommendations.append("Pattern has low historical success rate - review implementation")
        
        if factor_scores[ConfidenceFactor.USAGE_FREQUENCY] < 0.3:
            recommendations.append("Pattern rarely used - may need promotion or retirement")
        
        if factor_scores[ConfidenceFactor.RECENCY] < 0.5:
            recommendations.append("Pattern not recently used - verify still relevant")
        
        if sample_size < 10:
            recommendations.append("Limited usage history - confidence may improve with more data")
        
        if trend == 'declining':
            recommendations.append("Pattern performance declining - investigate root cause")
        
        return ConfidenceScore(
            overall_score=overall_score,
            factor_scores=factor_scores,
            reliability=reliability,
            sample_size=sample_size,
            last_updated=datetime.now(),
            trend=trend,
            recommendations=recommendations
        )
    
    def _calculate_historical_success(self, pattern_id: str) -> float:
        """Calculate score based on historical success rate"""
        if pattern_id not in self.pattern_performance:
            return 0.5  # Default neutral score
        
        perf = self.pattern_performance[pattern_id]
        
        # Base score is success rate
        base_score = perf.success_rate
        
        # Adjust for sample size (more confidence with more samples)
        if perf.total_uses < 5:
            confidence_factor = 0.5
        elif perf.total_uses < 20:
            confidence_factor = 0.8
        else:
            confidence_factor = 1.0
        
        # Weight recent performance more heavily
        recent_weight = 0.7
        overall_weight = 0.3
        
        recent_uses = [u for u in self.pattern_history.get(pattern_id, [])
                      if u.timestamp > datetime.now() - timedelta(days=30)]
        
        if recent_uses:
            recent_success_rate = sum(1 for u in recent_uses if u.success) / len(recent_uses)
            score = (recent_success_rate * recent_weight + base_score * overall_weight)
        else:
            score = base_score
        
        return score * confidence_factor
    
    def _calculate_pattern_completeness(self, pattern_data: Dict) -> float:
        """Calculate score based on pattern completeness"""
        required_fields = [
            'entities', 'global_requirements', 'workflow',
            'validations', 'infrastructure', 'description'
        ]
        
        optional_fields = [
            'integrations', 'dependencies', 'examples',
            'test_cases', 'performance_metrics'
        ]
        
        # Check required fields
        required_present = sum(1 for field in required_fields if field in pattern_data and pattern_data[field])
        required_score = required_present / len(required_fields)
        
        # Check optional fields (bonus)
        optional_present = sum(1 for field in optional_fields if field in pattern_data and pattern_data[field])
        optional_score = optional_present / len(optional_fields)
        
        # Weight required fields more heavily
        completeness_score = required_score * 0.8 + optional_score * 0.2
        
        # Check field quality
        quality_boost = 0
        
        if 'entities' in pattern_data and len(pattern_data['entities']) > 3:
            quality_boost += 0.05
        
        if 'validations' in pattern_data and len(pattern_data['validations']) > 2:
            quality_boost += 0.05
        
        if 'examples' in pattern_data and pattern_data['examples']:
            quality_boost += 0.1
        
        return min(completeness_score + quality_boost, 1.0)
    
    def _calculate_usage_frequency(self, pattern_id: str) -> float:
        """Calculate score based on usage frequency"""
        if pattern_id not in self.pattern_history:
            return 0.3  # Low score for unused patterns
        
        uses = self.pattern_history[pattern_id]
        
        # Calculate uses per month over last 6 months
        six_months_ago = datetime.now() - timedelta(days=180)
        recent_uses = [u for u in uses if u.timestamp > six_months_ago]
        
        if not recent_uses:
            return 0.2
        
        months_active = (datetime.now() - min(u.timestamp for u in recent_uses)).days / 30
        uses_per_month = len(recent_uses) / max(months_active, 1)
        
        # Score based on usage frequency
        if uses_per_month >= 10:
            return 1.0
        elif uses_per_month >= 5:
            return 0.8
        elif uses_per_month >= 2:
            return 0.6
        elif uses_per_month >= 1:
            return 0.4
        else:
            return 0.3
    
    def _calculate_recency_score(self, pattern_id: str) -> float:
        """Calculate score based on recency of use"""
        if pattern_id not in self.pattern_performance:
            return 0.5
        
        last_used = self.pattern_performance[pattern_id].last_used
        days_since_use = (datetime.now() - last_used).days
        
        # Decay function for recency
        if days_since_use <= 7:
            return 1.0
        elif days_since_use <= 30:
            return 0.8
        elif days_since_use <= 90:
            return 0.6
        elif days_since_use <= 180:
            return 0.4
        else:
            # Exponential decay after 6 months
            return max(0.2, 0.4 * math.exp(-days_since_use / 365))
    
    def _calculate_domain_alignment(self, pattern_data: Dict, context: Dict) -> float:
        """Calculate score based on domain alignment"""
        pattern_domain = pattern_data.get('domain', '')
        context_domain = context.get('domain', '')
        
        if not pattern_domain or not context_domain:
            return 0.5  # Neutral if no domain info
        
        # Direct match
        if pattern_domain == context_domain:
            return 1.0
        
        # Check for multi-domain patterns
        if pattern_data.get('multi_domain', False):
            supported_domains = pattern_data.get('supported_domains', [])
            if context_domain in supported_domains:
                return 0.9
        
        # Check for related domains
        domain_relationships = {
            'producer-portal': ['accounting', 'entity-integration'],
            'accounting': ['producer-portal', 'reinstatement'],
            'program-manager': ['program-traits'],
            'program-traits': ['program-manager']
        }
        
        related_domains = domain_relationships.get(pattern_domain, [])
        if context_domain in related_domains:
            return 0.6
        
        return 0.2  # Low score for mismatched domains
    
    def _calculate_complexity_match(self, pattern_data: Dict, context: Dict) -> float:
        """Calculate score based on complexity match"""
        pattern_complexity = self._assess_pattern_complexity(pattern_data)
        context_complexity = context.get('complexity', 'medium')
        
        complexity_levels = ['simple', 'medium', 'complex', 'very_complex']
        
        if pattern_complexity == context_complexity:
            return 1.0
        
        # Calculate distance
        try:
            pattern_idx = complexity_levels.index(pattern_complexity)
            context_idx = complexity_levels.index(context_complexity)
            distance = abs(pattern_idx - context_idx)
            
            # Score based on distance
            scores = [1.0, 0.7, 0.4, 0.2]
            return scores[min(distance, 3)]
        except ValueError:
            return 0.5  # Default if complexity not recognized
    
    def _assess_pattern_complexity(self, pattern_data: Dict) -> str:
        """Assess the complexity of a pattern"""
        complexity_score = 0
        
        # Check various complexity indicators
        if len(pattern_data.get('entities', [])) > 5:
            complexity_score += 2
        elif len(pattern_data.get('entities', [])) > 3:
            complexity_score += 1
        
        if len(pattern_data.get('integrations', [])) > 2:
            complexity_score += 2
        elif pattern_data.get('integrations'):
            complexity_score += 1
        
        if pattern_data.get('workflow', {}).get('steps', []):
            if len(pattern_data['workflow']['steps']) > 10:
                complexity_score += 2
            elif len(pattern_data['workflow']['steps']) > 5:
                complexity_score += 1
        
        if pattern_data.get('cross_domain', False):
            complexity_score += 2
        
        # Map score to complexity level
        if complexity_score >= 6:
            return 'very_complex'
        elif complexity_score >= 4:
            return 'complex'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'simple'
    
    def _calculate_validation_coverage(self, pattern_data: Dict) -> float:
        """Calculate score based on validation coverage"""
        validations = pattern_data.get('validations', {})
        
        if not validations:
            return 0.3  # Low score for no validations
        
        # Check validation completeness
        validation_types = ['structure', 'business_rules', 'data_integrity', 'security', 'performance']
        covered_types = sum(1 for vtype in validation_types if vtype in validations)
        
        type_coverage = covered_types / len(validation_types)
        
        # Check validation detail
        total_rules = sum(len(v.get('rules', [])) for v in validations.values())
        detail_score = min(total_rules / 10, 1.0)  # Cap at 10 rules
        
        # Check for test cases
        has_tests = any(v.get('test_cases') for v in validations.values())
        test_bonus = 0.2 if has_tests else 0
        
        return min(type_coverage * 0.5 + detail_score * 0.3 + test_bonus, 1.0)
    
    def _calculate_user_feedback_score(self, pattern_id: str) -> float:
        """Calculate score based on user feedback"""
        if pattern_id not in self.pattern_history:
            return 0.5  # Neutral score
        
        feedbacks = [u.feedback_score for u in self.pattern_history[pattern_id] 
                    if u.feedback_score is not None]
        
        if not feedbacks:
            return 0.5
        
        # Calculate average feedback score
        avg_feedback = statistics.mean(feedbacks)
        
        # Weight recent feedback more heavily
        recent_feedbacks = [
            u.feedback_score for u in self.pattern_history[pattern_id]
            if u.feedback_score is not None and 
            u.timestamp > datetime.now() - timedelta(days=90)
        ]
        
        if recent_feedbacks:
            recent_avg = statistics.mean(recent_feedbacks)
            # 70% recent, 30% overall
            weighted_score = recent_avg * 0.7 + avg_feedback * 0.3
        else:
            weighted_score = avg_feedback
        
        return weighted_score
    
    def _calculate_reliability(self, pattern_id: str, factor_scores: Dict[ConfidenceFactor, float]) -> float:
        """Calculate how reliable the confidence score is"""
        reliability_factors = []
        
        # Sample size reliability
        sample_size = len(self.pattern_history.get(pattern_id, []))
        if sample_size >= 50:
            sample_reliability = 1.0
        elif sample_size >= 20:
            sample_reliability = 0.8
        elif sample_size >= 10:
            sample_reliability = 0.6
        elif sample_size >= 5:
            sample_reliability = 0.4
        else:
            sample_reliability = 0.2
        
        reliability_factors.append(sample_reliability)
        
        # Consistency reliability (low variance in scores)
        if factor_scores:
            score_variance = statistics.variance(factor_scores.values()) if len(factor_scores) > 1 else 0
            consistency_reliability = 1.0 - min(score_variance * 2, 0.8)  # High variance reduces reliability
            reliability_factors.append(consistency_reliability)
        
        # Recency reliability
        recency_score = factor_scores.get(ConfidenceFactor.RECENCY, 0.5)
        reliability_factors.append(recency_score)
        
        # Confidence accuracy (how well past confidence predictions matched outcomes)
        if pattern_id in self.pattern_performance:
            accuracy = self.pattern_performance[pattern_id].confidence_accuracy
            reliability_factors.append(accuracy)
        
        return statistics.mean(reliability_factors) if reliability_factors else 0.5
    
    def _determine_trend(self, pattern_id: str) -> str:
        """Determine performance trend for a pattern"""
        if pattern_id not in self.pattern_performance:
            return 'stable'
        
        usage_trend = self.pattern_performance[pattern_id].usage_trend
        
        if len(usage_trend) < 5:
            return 'stable'  # Not enough data
        
        # Look at recent performance
        recent_trend = usage_trend[-10:]  # Last 10 uses
        recent_success_rate = sum(1 for _, success in recent_trend if success) / len(recent_trend)
        
        # Compare with overall success rate
        overall_rate = self.pattern_performance[pattern_id].success_rate
        
        if recent_success_rate > overall_rate + 0.1:
            return 'improving'
        elif recent_success_rate < overall_rate - 0.1:
            return 'declining'
        else:
            return 'stable'
    
    def update_pattern_usage(self, pattern_id: str, success: bool, 
                           context: Dict, confidence_at_time: float,
                           actual_outcome: Optional[str] = None,
                           feedback_score: Optional[float] = None):
        """
        Record pattern usage and update performance metrics
        
        Args:
            pattern_id: Pattern identifier
            success: Whether the pattern was successfully applied
            context: Usage context
            confidence_at_time: Confidence score when pattern was used
            actual_outcome: Actual outcome description
            feedback_score: User feedback score (0-1)
        """
        usage = PatternUsage(
            pattern_id=pattern_id,
            timestamp=datetime.now(),
            success=success,
            context=context,
            confidence_at_time=confidence_at_time,
            actual_outcome=actual_outcome,
            feedback_score=feedback_score
        )
        
        self.pattern_history[pattern_id].append(usage)
        
        # Update performance metrics
        self._update_performance_metrics(pattern_id)
        
        # Update confidence accuracy
        self._update_confidence_accuracy(pattern_id, success, confidence_at_time)
        
        logger.info(f"Updated usage for pattern {pattern_id}: success={success}, confidence={confidence_at_time:.2f}")
    
    def _update_performance_metrics(self, pattern_id: str):
        """Update performance metrics for a pattern"""
        if pattern_id not in self.pattern_history:
            return
        
        uses = self.pattern_history[pattern_id]
        total_uses = len(uses)
        successful_uses = sum(1 for u in uses if u.success)
        
        if total_uses == 0:
            return
        
        success_rate = successful_uses / total_uses
        average_confidence = statistics.mean(u.confidence_at_time for u in uses)
        
        # Calculate confidence accuracy
        confidence_errors = []
        for use in uses:
            expected_success = use.confidence_at_time
            actual_success = 1.0 if use.success else 0.0
            error = abs(expected_success - actual_success)
            confidence_errors.append(error)
        
        confidence_accuracy = 1.0 - statistics.mean(confidence_errors) if confidence_errors else 0.5
        
        # Update usage trend
        usage_trend = [(u.timestamp, u.success) for u in sorted(uses, key=lambda x: x.timestamp)][-50:]  # Keep last 50
        
        self.pattern_performance[pattern_id] = PatternPerformance(
            pattern_id=pattern_id,
            total_uses=total_uses,
            successful_uses=successful_uses,
            success_rate=success_rate,
            average_confidence=average_confidence,
            confidence_accuracy=confidence_accuracy,
            usage_trend=usage_trend,
            last_used=max(u.timestamp for u in uses)
        )
    
    def _update_confidence_accuracy(self, pattern_id: str, actual_success: bool, predicted_confidence: float):
        """Update confidence accuracy using exponential moving average"""
        if pattern_id in self.pattern_performance:
            # Calculate accuracy for this prediction
            predicted_success = predicted_confidence
            actual = 1.0 if actual_success else 0.0
            prediction_accuracy = 1.0 - abs(predicted_success - actual)
            
            # Update with exponential moving average
            current_accuracy = self.pattern_performance[pattern_id].confidence_accuracy
            new_accuracy = (1 - self.learning_rate) * current_accuracy + self.learning_rate * prediction_accuracy
            
            self.pattern_performance[pattern_id].confidence_accuracy = new_accuracy
    
    def get_pattern_recommendations(self, pattern_id: str) -> List[str]:
        """Get improvement recommendations for a pattern"""
        recommendations = []
        
        if pattern_id not in self.pattern_performance:
            recommendations.append("No usage history - encourage pattern adoption")
            return recommendations
        
        perf = self.pattern_performance[pattern_id]
        
        # Success rate recommendations
        if perf.success_rate < 0.5:
            recommendations.append(f"Low success rate ({perf.success_rate:.2f}) - review pattern implementation")
        elif perf.success_rate < 0.7:
            recommendations.append(f"Moderate success rate ({perf.success_rate:.2f}) - identify failure patterns")
        
        # Usage recommendations
        if perf.total_uses < 10:
            recommendations.append("Limited usage data - promote pattern or consider retirement")
        
        # Confidence accuracy recommendations
        if perf.confidence_accuracy < 0.6:
            recommendations.append("Poor confidence predictions - recalibrate scoring factors")
        
        # Trend recommendations
        trend = self._determine_trend(pattern_id)
        if trend == 'declining':
            recommendations.append("Performance declining - investigate recent failures")
        elif trend == 'improving':
            recommendations.append("Performance improving - document successful adaptations")
        
        # Recency recommendations
        days_unused = (datetime.now() - perf.last_used).days
        if days_unused > 90:
            recommendations.append(f"Not used in {days_unused} days - verify pattern relevance")
        
        return recommendations
    
    def export_confidence_report(self, pattern_id: str, pattern_data: Dict, context: Dict) -> Dict:
        """Generate detailed confidence analysis report"""
        confidence = self.calculate_confidence(pattern_id, pattern_data, context)
        
        report = {
            'pattern_id': pattern_id,
            'timestamp': datetime.now().isoformat(),
            'overall_confidence': confidence.overall_score,
            'reliability': confidence.reliability,
            'sample_size': confidence.sample_size,
            'trend': confidence.trend,
            'factor_breakdown': {
                factor.value: {
                    'score': score,
                    'weight': self.confidence_weights[factor],
                    'contribution': score * self.confidence_weights[factor]
                }
                for factor, score in confidence.factor_scores.items()
            },
            'recommendations': confidence.recommendations,
            'performance_history': None,
            'improvement_suggestions': self.get_pattern_recommendations(pattern_id)
        }
        
        # Add performance history if available
        if pattern_id in self.pattern_performance:
            perf = self.pattern_performance[pattern_id]
            report['performance_history'] = {
                'total_uses': perf.total_uses,
                'success_rate': perf.success_rate,
                'average_confidence': perf.average_confidence,
                'confidence_accuracy': perf.confidence_accuracy,
                'last_used': perf.last_used.isoformat(),
                'recent_performance': [
                    {'timestamp': t.isoformat(), 'success': s}
                    for t, s in perf.usage_trend[-10:]  # Last 10 uses
                ]
            }
        
        return report
    
    def save_historical_data(self):
        """Save historical data to disk"""
        try:
            # Ensure directory exists
            self.history_path.mkdir(parents=True, exist_ok=True)
            
            # Save usage history
            history_data = {}
            for pattern_id, usages in self.pattern_history.items():
                history_data[pattern_id] = [
                    {
                        'pattern_id': u.pattern_id,
                        'timestamp': u.timestamp.isoformat(),
                        'success': u.success,
                        'context': u.context,
                        'confidence_at_time': u.confidence_at_time,
                        'actual_outcome': u.actual_outcome,
                        'feedback_score': u.feedback_score
                    }
                    for u in usages
                ]
            
            with open(self.history_path / "pattern-usage-history.json", 'w') as f:
                json.dump(history_data, f, indent=2)
            
            # Save performance data
            performance_data = {}
            for pattern_id, perf in self.pattern_performance.items():
                performance_data[pattern_id] = {
                    'total_uses': perf.total_uses,
                    'successful_uses': perf.successful_uses,
                    'success_rate': perf.success_rate,
                    'average_confidence': perf.average_confidence,
                    'confidence_accuracy': perf.confidence_accuracy,
                    'usage_trend': [[t.isoformat(), s] for t, s in perf.usage_trend],
                    'last_used': perf.last_used.isoformat()
                }
            
            with open(self.history_path / "pattern-performance.json", 'w') as f:
                json.dump(performance_data, f, indent=2)
            
            logger.info(f"Saved historical data for {len(self.pattern_history)} patterns")
            
        except Exception as e:
            logger.error(f"Error saving historical data: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Initialize scorer
    scorer = ConfidenceScorer("/app/workspace/requirements/shared-infrastructure/knowledge-base")
    
    # Example pattern data
    pattern_data = {
        'domain': 'producer-portal',
        'entities': ['driver', 'vehicle', 'quote', 'policy'],
        'global_requirements': ['GR-52', 'GR-44', 'GR-41'],
        'workflow': {
            'steps': ['collect_info', 'validate', 'calculate', 'generate_quote', 'bind_policy']
        },
        'validations': {
            'structure': {'rules': ['schema_validation', 'required_fields']},
            'business_rules': {'rules': ['age_check', 'coverage_limits']},
            'data_integrity': {'rules': ['duplicate_check', 'consistency_validation']}
        },
        'integrations': ['DCS', 'rating_engine'],
        'infrastructure': {
            'database': ['drivers', 'vehicles', 'quotes'],
            'api': ['/quotes', '/policies']
        },
        'examples': ['example1', 'example2'],
        'test_cases': ['test1', 'test2']
    }
    
    # Example context
    context = {
        'domain': 'producer-portal',
        'complexity': 'medium',
        'requirement_type': 'quote_binding',
        'priority': 'high'
    }
    
    # Calculate confidence
    pattern_id = "quote_binding_pattern_v2"
    confidence = scorer.calculate_confidence(pattern_id, pattern_data, context)
    
    print(f"Pattern: {pattern_id}")
    print(f"Overall Confidence: {confidence.overall_score:.2f}")
    print(f"Reliability: {confidence.reliability:.2f}")
    print(f"Sample Size: {confidence.sample_size}")
    print(f"Trend: {confidence.trend}")
    
    print("\nFactor Breakdown:")
    for factor, score in confidence.factor_scores.items():
        weight = scorer.confidence_weights[factor]
        contribution = score * weight
        print(f"  {factor.value}: {score:.2f} (weight: {weight:.2f}, contribution: {contribution:.2f})")
    
    print("\nRecommendations:")
    for rec in confidence.recommendations:
        print(f"  - {rec}")
    
    # Simulate pattern usage
    print("\n\nSimulating pattern usage...")
    scorer.update_pattern_usage(
        pattern_id=pattern_id,
        success=True,
        context=context,
        confidence_at_time=confidence.overall_score,
        feedback_score=0.85
    )
    
    # Get pattern recommendations
    print("\nPattern Improvement Recommendations:")
    improvements = scorer.get_pattern_recommendations(pattern_id)
    for imp in improvements:
        print(f"  - {imp}")
    
    # Generate report
    print("\n\nGenerating confidence report...")
    report = scorer.export_confidence_report(pattern_id, pattern_data, context)
    print(f"Report generated with {len(report['factor_breakdown'])} factors analyzed")