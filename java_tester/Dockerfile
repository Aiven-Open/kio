FROM gradle:jdk17 AS build

RUN mkdir /java_tester
WORKDIR /java_tester
ADD src src
ADD build.gradle build.gradle

RUN gradle --no-daemon distTar && tar -xvf build/distributions/java_tester.tar

FROM eclipse-temurin:17-jre
COPY --from=build /java_tester/java_tester /java_tester

CMD /java_tester/bin/java_tester
