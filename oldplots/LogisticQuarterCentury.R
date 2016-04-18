library(scales)
l <- read.csv('~/Dropbox/GenreProject/python/reception/poetry/1845apredictions.csv')
l$birthdate[l$birthdate < 1700] <- NA
l$reviewed[l$reviewed == 'addedbecausecanon'] <- NA
pastthreshold = 1845
futurethreshold = 1869
model = glm(data = filter(l, pubdate >= pastthreshold, pubdate <= futurethreshold), 
            formula = as.integer(reviewed == 'rev') ~ logistic + pubdate, family = binomial(logit))
intercept = coef(model)[1] / (-coef(model)[2])
slope = coef(model)[3] / (-coef(model)[2])
line = intercept + (slope * l$pubdate)
true = sum(l$logistic > line & l$reviewed == 'rev', na.rm = TRUE) + sum(l$logistic <= line & l$reviewed == 'not', na.rm = TRUE)
false = sum(l$logistic < line & l$reviewed == 'rev', na.rm = TRUE) + sum(l$logistic >= line & l$reviewed == 'not', na.rm = TRUE)
print(true / (true + false))
levels(l$reviewed) = c('random', 'reviewed')
p <- ggplot(l, aes(x = pubdate, y = logistic, color = reviewed, shape = reviewed)) + 
  geom_point() + geom_abline(intercept = intercept, slope = slope) + scale_shape(name="actually") + 
  scale_color_manual(name = "actually", values = c('gray64', 'red3')) + 
  theme(text = element_text(size = 16)) + 
  scale_y_continuous('Predicted probability of coming from reviewed set\n', labels = percent, breaks = c(0.25,0.5,0.75)) + 
  scale_x_continuous("")
plot(p)